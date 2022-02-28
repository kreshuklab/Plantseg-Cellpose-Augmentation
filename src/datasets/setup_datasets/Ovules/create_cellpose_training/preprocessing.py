import os
import argparse
import skimage.io
import numpy as np
import h5py

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
    return filename.split('.')[0].replace('_', '')

def read_h5(dir_path, filename):
    with h5py.File(os.path.join(dir_path, filename), 'r') as f:
        raw = f['raw'][:]
        label = f['label'][:]
    return raw, label

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
                files.append((raw_file, label_file))
    return files

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--original_dir', type=str)
    parser.add_argument('--dst_dir', type=str)
    parser.add_argument('--max_slice', type=int, default= -1 )
    args = parser.parse_args()

    # Assert all exist
    assert os.path.isdir(args.original_dir), "label dir must exist"
    assert os.path.isdir(args.dst_dir), "Dst dir must exist"
    
    # Go through files in label
    for sub_dir in os.listdir(args.original_dir):
        if not os.path.isdir(os.path.join(args.original_dir, sub_dir)): continue
        for filename in os.listdir(os.path.join(args.original_dir, sub_dir)):    
            # IF not h5 continut
            if not get_extention(filename)=='h5': continue
            # Read file
            raw, label = read_h5(os.path.join(args.original_dir, sub_dir), filename)   
            ## Loop through slices
            for z_slice in range(len(label)):  
                if z_slice == args.max_slice: break
                ### Name slice
                new_raw_file = getFileName(filename) + '_slice'+str(z_slice).zfill(3) + '_raw.tif'
                new_label_file = getFileName(filename) + '_slice'+str(z_slice).zfill(3) + '_label.tif'
                ### Save slice in dst
                skimage.io.imsave(os.path.join(args.dst_dir, new_raw_file), raw[z_slice: z_slice+1])
                skimage.io.imsave(os.path.join(args.dst_dir, new_label_file), label[z_slice: z_slice+1])

    






