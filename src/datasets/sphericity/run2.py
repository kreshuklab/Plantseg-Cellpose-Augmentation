import argparse
import os
from statistics import mean
import numpy as np
from skimage.segmentation import find_boundaries
import pyvista as pv
import skimage.io
import pandas as pd
import sys
import logging

DATASET_PATH = '/scratch/ottosson/datasets'

def bbox2_3D(img):
    r = np.any(img, axis=(1, 2))
    c = np.any(img, axis=(0, 2))
    z = np.any(img, axis=(0, 1))

    rmin, rmax = np.where(r)[0][[0, -1]]
    cmin, cmax = np.where(c)[0][[0, -1]]
    zmin, zmax = np.where(z)[0][[0, -1]]

    return img[rmin:rmax+1,cmin:cmax+1,zmin:zmax+1]


def cell_spericity(cell):
    bound_map = find_boundaries(cell, mode = 'inner')
    if bound_map.ndim != 3:
        print("Cell is ", bound_map.ndim, " None is returned, size ", np.sum(bound_map))
        return None
    cell_boundary = np.array(bound_map.nonzero(), dtype = 'float32').T
    mesh = pv.PolyData(cell_boundary).reconstruct_surface()
    sphericity = np.power(np.pi*36*mesh.volume**2, 1/3)/mesh.area
    return sphericity


def image_spericity(im, background_labels = None):
    if background_labels is None:
        background_labels = [0,1]
    labels = np.unique(im)
    sphericities = []
    len_labels = len(labels)
    for i,label in enumerate(labels):
        if label in background_labels: continue
        cell = im == label
        s = cell_spericity(bbox2_3D(cell))
        sphericities.append(s)
    return sphericities

def folder_spericity(folder_path, background_labels = None):
    if background_labels is None:
        background_labels = [0,1]
    sphericities = dict()
    for i,filename in enumerate(os.listdir(folder_path)):
        logger.info(f"{i}/{len(os.listdir(folder_path))}: start processing {filename}")
        if filename.split('.')[-1] != 'tif': continue
        sample_name = filename.split('_')[0]
        im = skimage.io.imread(os.path.join(folder_path, filename))
        sphericities[sample_name] = image_spericity(im, background_labels = background_labels)
    return sphericities

def img_list_spericity(im_list,background_labels = None):
    if background_labels is None:
        background_labels = [0,1]
    sphericities = dict()
    num_image = len(im_list)
    for i,im_path in enumerate(im_list):
        logger.info(f"{i}/{num_image}: start processing {im_path}")
        if im_path.split('.')[-1] != 'tif': continue
        sample_name = im_path.split('/')[-1].split('_')[0]
        im = skimage.io.imread(im_path)
        sphericities[sample_name] = image_spericity(im, background_labels = background_labels)
    return sphericities

def ov_spher():
    parser = argparse.ArgumentParser()
    parser.add_argument('--node_id', type=int)
    parser.add_argument('--num_nodes', type=int)
    args = parser.parse_args()

    ov_path = '/scratch/ottosson/datasets/Ovules/label'
    im_list = os.listdir(ov_path)
    part_len = len(im_list)//args.num_nodes

    if  part_len*(args.node_id+1) > len(im_list):
        node_list = im_list[part_len*args.node_id:]
    else:
        node_list = im_list[part_len*args.node_id:part_len*(args.node_id+1)]
    node_list = [os.path.join(ov_path,im_path) for im_path in node_list]
    logger.info(node_list)
    sphers_dict =  img_list_spericity(node_list)

    means = dict()
    stds = dict()
    totals = []
    for k,v in sphers_dict.items():
        means[k]= np.nanmean(v)
        stds[k]= np.nanstd(v)
        totals.extend(v)

    BASE_PATH = '/scratch/ottosson/datasets/Ovules/dataframes/tmep'
    save_path = os.path.join(BASE_PATH,'spher_total_' + str(args.node_id) + '.csv')
    pd.DataFrame(data = {'sphericity': totals}).to_csv(save_path, index = False)

    save_path = os.path.join(BASE_PATH,'spher_means_' + str(args.node_id) + '.csv')
    pd.DataFrame(data = [means, stds], index = ['mean', 'std']).to_csv(save_path)




def run_and_save():  
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset')
    args = parser.parse_args()
    label_path = os.path.join(DATASET_PATH,
                             args.dataset,
                            'label')
    sphers_dict = folder_spericity(label_path, background_labels=[0,1])
    means = dict()
    stds = dict()
    totals = []
    for k,v in sphers_dict.items():
        means[k]= np.nanmean(v)
        stds[k]= np.nanstd(v)
        totals.extend(v)

    
    save_path = os.path.join(DATASET_PATH,args.dataset, 'dataframes','spher_total.csv')
    pd.DataFrame(data = {'sphericity': totals}).to_csv(save_path, index = False)


    save_path = os.path.join(DATASET_PATH,args.dataset, 'dataframes','spher_means.csv')
    pd.DataFrame(data = [means, stds], index = ['mean', 'std']).to_csv(save_path)


def test_cell():
    label = skimage.io.imread('/scratch/ottosson/datasets/Ovules/label/N422ds2x_label.tif')
    cell = label == 2
    sphericity = cell_spericity(cell)
    print(sphericity)  

def test_image():
    label = skimage.io.imread('/scratch/ottosson/datasets/Ovules/label/N422ds2x_label.tif')
    sphericity = image_spericity(label)
    print(sphericity)  

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Logging to console
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s [%(threadName)s] %(levelname)s %(name)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


if __name__ == '__main__':
    ov_spher()




