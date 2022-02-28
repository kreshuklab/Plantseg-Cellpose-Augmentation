import skimage.io
import h5py
import os
from os.path import join
import argparse
import numpy as np

def describe(im):
    print(f"\tdtype: {im.dtype}")
    print(f"\tshape: {im.shape}")
    print(f"\tmin: {im.min()}")
    print(f"\tmean: {im.mean()}")
    print(f"\tmax: {im.max()}")

def get_extention(filename):
    return filename.split('.')[-1]

def getFileType(filename):
    return filename.split('.')[0].split('_')[-1]

def isLabel(filename):
    return getFileType(filename) == 'label'

def isRaw(filename):
    return getFileType(filename) == 'raw'

def getFileName(filename):
    return filename.split('_')[0]

def find_matching_files(raw_dir, label_dir, file_ext = None):
    files =[]
    for raw_file in os.listdir(raw_dir):
        raw_name = getFileName(raw_file)
        if file_ext and file_ext != get_extention(raw_file):
            continue
        for label_file in os.listdir(label_dir):
            if file_ext and file_ext != get_extention(label_file):
                continue
            label_name = getFileName(label_file)
            if raw_name == label_name:
                files.append((raw_name, raw_file, label_file))
    return files

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path')
    parser.add_argument('--num_val', type=int, default=2)
    args = parser.parse_args()

    # Create paths to raw and label and training
    raw_path = join(args.dataset_path, 'raw')
    label_path = join(args.dataset_path, 'label')
    plantseg_path = join(args.dataset_path, 'plantseg_training')
    
    # check if paths are valid
    assert os.path.isdir(raw_path), "Raw path is not a directory"
    assert os.path.isdir(label_path), "Label path is not a directory"
    assert os.path.isdir(plantseg_path), "Plantseg path is not a directory"
    # create train and val folders
    train_path = join(plantseg_path, 'train')
    if not os.path.isdir(train_path):
        os.mkdir(train_path)
    else:
        print('Train folder already present')
    val_path = join(plantseg_path, 'val')
    if not os.path.isdir(val_path):
        os.mkdir(val_path)
    else:
        print('Val folder already present')
    
    # find matches in raw and label
    matching_files = find_matching_files(raw_path, label_path, file_ext='tif')
    # Set some of the file to the validation folder
    val_index = np.random.choice(len(matching_files), size=args.num_val, replace = False)
    # go through matches and save them in trainign
    for i,(file_name, raw_file, label_file) in enumerate(matching_files):
        # open files
        raw = skimage.io.imread(join(raw_path, raw_file))
        label = skimage.io.imread(join(label_path, label_file))
        # Set dataset type
        dataset_folder = 'val' if i in val_index else 'train'
        # save files
        plantseg_file = file_name +'_h5.h5'
        with h5py.File(join(plantseg_path,dataset_folder, plantseg_file), 'w') as f:
            f.create_dataset('raw', data=raw)
            f.create_dataset('label', data=label)









