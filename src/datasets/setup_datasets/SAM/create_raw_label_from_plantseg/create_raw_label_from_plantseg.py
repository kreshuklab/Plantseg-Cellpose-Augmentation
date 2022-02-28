

import argparse
import os
from os.path import join
import h5py
import skimage.io

def read_h5(dir_path, filename):
    with h5py.File(join(dir_path, filename), 'r') as f:
        raw = f['raw'][:]
        label = f['label'][:]
    return raw, label

def get_extention(filename):
    return filename.split('.')[-1]

def get_name(filename):
    return filename.split('_')[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--plantseg_path')
    parser.add_argument('--dataset_path')
    args = parser.parse_args()

    assert os.path.isdir(args.plantseg_path), "Plantseg path must exist"
    assert os.path.isdir(args.dataset_path), "Data path must exist"
    assert os.path.isdir(join(args.dataset_path,'raw')), "Raw path must exist"
    assert os.path.isdir(join(args.dataset_path,'label')), "Lable path must exist"

    for sub_dir in os.listdir(args.plantseg_path):
        if not os.path.isdir(join(args.plantseg_path, sub_dir)): continue
        for filename in os.listdir(join(args.plantseg_path, sub_dir)):
            if get_extention(filename) != 'h5': continue
            raw, label = read_h5(join(args.plantseg_path, sub_dir), filename)
            raw_name = get_name(filename) + '_raw.tif'
            label_name = get_name(filename) + '_label.tif'
            skimage.io.imsave(join(args.dataset_path, 'raw', raw_name), raw)
            skimage.io.imsave(join(args.dataset_path, 'label', label_name), label)
            






