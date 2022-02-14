#from distutils.command.config import config
from curses import meta
import os
from os.path import join
from unittest import result
import skimage.io
from skimage.metrics import variation_of_information,adapted_rand_error,contingency_table
from collections import defaultdict
import pandas as pd
import argparse
import jseg.evaluation
import numpy as np
import h5py
import jutil

from datetime import datetime

def evaluate_segmentation(ground_truth, prediction, metadata):
    data = {}
    for k,v in metadata.items():
        data[k] = v
    # general data
    num_gt = len(np.unique(ground_truth))-1
    num_pr = len(np.unique(prediction))-1
    data['num-cells'] = num_gt 

    ignore_labels = (0,1)
    background_label = 1
    # Variation of information
    over_seg, under_seg = variation_of_information(ground_truth, prediction, ignore_labels = ignore_labels)
    data['VoI-over'] = over_seg
    data['VoI-under'] = under_seg
    data['VoI'] = over_seg + under_seg
    
    # addaptive random error
    are, prec, rec = adapted_rand_error(image_true=ground_truth, image_test=prediction, ignore_labels=ignore_labels)
    data['ar-error'] = are
    data['ar-precision'] = prec
    data['ar-recall'] = rec 

    # Voumetric 
    #vji = jseg.evaluation.get_vji(ground_truth, prediction, background_label)
    #data['Volumetric-Jaccard'] = vji

    # quality
    full_conttable = contingency_table(im_true = ground_truth, im_test= prediction, normalize=False)
    (correct_rate, over_rate, under_rate, miss_rate, divergent_rate) = jseg.evaluation.segmentation_type(full_conttable, num_gt, background_label=background_label)
    data['qual-correct'] = correct_rate
    data['qual-over'] = over_rate
    data['qual-under'] = under_rate
    data['qual-miss'] = miss_rate
    data['qual-divergent'] = divergent_rate   

    return data

def read_tif(file_path):
    return skimage.io.imread(file_path)

def read_h5(file_path, datasets):
    ims = []
    with h5py.File(file_path, 'r') as f:
        if datasets is None:
            print("Datasets in file: ", f.keys())
            return 
        for dataset in datasets:
            ims.append(f[dataset][:])
    if len(ims) == 1:
        return ims[0]
    return ims

def get_extention(file_path):
    return file_path.split('.')[-1]

def read_file(file_path, datasets = None):
    ext = get_extention(file_path)
    if ext == 'tif': return read_tif(file_path)
    if ext == 'h5': return read_h5(file_path, datasets)
    assert False, "Please provide a valid file"


def getType(filename):
    return filename.split('.')[0].split('_')[-1]
def getName(filename):
    return filename.split('.')[0].split('_')[0]
def isRaw(filename):
    return getType(filename) == 'raw'
def isLabel(filename):
    return getType(filename) == 'label'
def isPred(filename):
    return getType(filename) == 'pred'
     

def eval_dataset(label_path, pred_path, metadata):
    # find matches
    matched_names = []
    for label_name in os.listdir(label_path):
        if not isLabel(label_name): continue
        for pred_name in os.listdir(pred_path):
            if not isPred(pred_name): continue
            if getName(label_name) == getName(pred_name):
                matched_names.append((label_name, pred_name))

    # go through matches
    result = list()
    for label_name, pred_name in matched_names:
        print(f"\tsample: {getName(label_name)}")
        label = skimage.io.imread(os.path.join(label_path, label_name))
        pred = skimage.io.imread(os.path.join(pred_path, pred_name))

        ## evaluate
        metadata['sample_name'] = getName(label_name)
        result.append(evaluate_segmentation(label, pred, metadata))
    return result

def main(config_setup = None):
    result =list()
    metadata = dict()
    metadata['trainset'] = config_setup['trainset']
    metadata['exp_id'] = config_setup['exp_id']
    for predset in config_setup['predsets']:
        now = datetime.now()
        config_setup['eval_' + predset + '_start'] = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)} {str(now.hour).zfill(2)}:{str(now.month).zfill(2)}"
        
        print(f"Evaluating on dataset {predset}:")
        label_path = config_setup['labelset_paths'][predset]
        pred_path = join(config_setup['predictions_path'],predset)
        metadata['predset'] = predset
        result.extend(eval_dataset(label_path, pred_path, metadata))
        now = datetime.now()
        config_setup['pred_' + predset + '_end'] = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)} {str(now.hour).zfill(2)}:{str(now.month).zfill(2)}"
        jutil.save_yml(os.path.join(config_setup['configs_path'],'config_setup.yml'), config_setup)
        
    df = pd.json_normalize(result)
    df.to_csv(join(config_setup['results_path'],'result.csv'), index = False)
    # eval_dataset
    ## evaluate_segmentaition



import time
if __name__ == '__main__':
    # parse input
    parser = argparse.ArgumentParser(description='Evaluation')
    parser.add_argument('--config_setup', type=str)
    args = parser.parse_args()
    config_setup = jutil.load_yml(args.config_setup)

    main(config_setup = config_setup)
    

