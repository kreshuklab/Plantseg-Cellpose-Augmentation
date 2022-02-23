import os
from sqlite3 import connect
from skimage import io
from skimage.metrics import variation_of_information
from collections import defaultdict
from jseg import utils
import pandas as pd
import numpy as np

import scipy.ndimage as nd
import pandas as pd
from collections import defaultdict

SEGMENTATION_TYPES = ["extra-segmentation",
                      "missed-segmentation",
                      "correct-segmentation",
                      "over-segmentation",
                      "under-segmentation",
                      "divergent-segmentation",
                      ]


def get_vji(ground_truth, prediction, background_label):
    """Vlumetric jaccard index
    """
    gt_unique = np.unique(ground_truth)
    pr_unique = np.unique(prediction)
    total_g = 0
    total_val = 0
    for g in gt_unique:
        if g == background_label: continue
        g_coords = np.where(ground_truth == g)
        g_set = set((coord) for coord in zip(*g_coords))
        total_g += len(g_set)
        best_p = 1
        best_val = 0
        for p in pr_unique:
            if p == background_label: continue
            p_coords = np.where(prediction == p)
            p_set = set((coord) for coord in zip(*p_coords))
            val = len(g_set)*len(g_set.intersection(p_set))/len(g_set.union(p_set))
            if val >= best_val:
                best_val = val
                best_p = p

        total_val += best_val
    return total_val / total_g


def segmentation_type(cont_table, num_grund_truth, background_label):
    clusters = create_clusters(cont_table, background_label)
    # correct
    num_correct = count_kv(clusters,'ground_truth', 'segmentation-type' ,'correct-segmentation',background_label)
    num_over =  count_kv(clusters,'ground_truth','segmentation-type' ,'over-segmentation',background_label)
    num_under = count_kv(clusters,'ground_truth','segmentation-type' ,'under-segmentation',background_label)
    num_missed = count_kv(clusters,'ground_truth','segmentation-type' ,'missed-segmentation',background_label)
    num_divergent = count_kv(clusters,'ground_truth','segmentation-type' ,'divergent-segmentation',background_label)
    
    return (num_correct/num_grund_truth,
           num_over/num_grund_truth,
           num_under/num_grund_truth,
           num_missed/num_grund_truth,
           num_divergent/num_grund_truth)

def count_kv(lis, count_key, cat_key, cat_val, background_label):
    count = 0
    for d in lis:
        if d[cat_key] == cat_val:
            count += len(d[count_key])
            if background_label in d[count_key]:
                count -= 1
    return count

def get_count_of_key_in_list(lis,key):
    count = 0
    for dic in lis:
        count += len(dic[key])
    return count
    
def create_clusters(cont_table, background_label):   
    connections = create_connections(cont_table)
    # Remove any connection with label background
    if (background_label, background_label) in connections:
        connections.remove((background_label, background_label))
    # Cluster the connections with special case for background connections
    clusters = []
    for g,p in connections:
        g_match = False
        p_match = False
        if g != background_label:
            for ci_g,cluster in enumerate(clusters):
                if not cluster['ground_truth'].isdisjoint([g]):
                    g_match = True
                    break 
        if p != background_label:
            for ci_p, cluster in enumerate(clusters):
                if not cluster['prediction'].isdisjoint([p]):
                    p_match = True
                    break
        if not g_match and not p_match:
            clusters.append({'ground_truth':{g},'prediction': {p}})
        elif g_match and not p_match:
            clusters[ci_g]['ground_truth'].update([g])
            clusters[ci_g]['prediction'].update([p])
        elif not g_match and p_match:
            clusters[ci_p]['ground_truth'].update([g])
            clusters[ci_p]['prediction'].update([p])
        elif ci_g == ci_p:
            # They are the same
            clusters[ci_g]['ground_truth'].update([g])
            clusters[ci_g]['prediction'].update([p])
        elif ci_g != ci_p:
            base_index = min(ci_g, ci_p)
            append_index = max(ci_g, ci_p)
            append_cluster = clusters.pop(append_index)
            clusters[base_index]['ground_truth'].update(append_cluster['ground_truth'])
            clusters[base_index]['prediction'].update(append_cluster['prediction']) 
    # label the different clusters
    for cluster in clusters:
        num_gs = len(cluster['ground_truth'])
        num_ps = len(cluster['prediction'])
        bg_in_gs = background_label in cluster['ground_truth']
        bg_in_ps = background_label in cluster['prediction']
        assert num_gs > 0, "Most be atleast one ground node in cluster"
        assert num_ps > 0, "Most be atleast one prediction node in cluster"
        assert not (bg_in_gs and bg_in_ps), "Background can't be in both" 
        if num_gs == 1 and num_ps == 1: 
            if bg_in_gs:
                cluster['segmentation-type'] = "extra-segmentation"
            elif bg_in_ps:
                cluster['segmentation-type'] = "missed-segmentation"
            else:
                cluster['segmentation-type'] = "correct-segmentation"
        elif bg_in_gs or bg_in_ps:
            cluster['segmentation-type'] = "divergent-segmentation"
        elif num_gs == 1 and num_ps > 1:
            cluster['segmentation-type'] = "over-segmentation"
        elif num_gs > 1 and num_ps == 1:
            cluster['segmentation-type'] = "under-segmentation"
        else:
            cluster['segmentation-type'] = "divergent-segmentation"
    return clusters





def get_best_matches(cont_table):
    """ Return the mapping from ground truth to the best prediction and vice versa.
    """
    g2p = dict()
    g2max = defaultdict(int)
    p2g = dict()
    p2max = defaultdict(int)
    for g, p, val in zip(cont_table.tocoo().row,
                         cont_table.tocoo().col,
                         cont_table.tocoo().data):
        if val >= g2max[g]:
            g2max[g] = val
            g2p[g] = p
        if val >= p2max[p]:
            p2max[p] = val
            p2g[p] = g   
    return g2p, p2g



def create_connections(cont_table):
    """ Return a set of all connections in a continguency table
    """
    g2p, p2g = get_best_matches(cont_table)
    # create connections
    connections = set()
    temp_con = []
    for g,p in g2p.items():
        temp_con.append((g,p))

    for p,g in p2g.items():
        temp_con.append((g,p))
    connections.update(temp_con)
    return connections

