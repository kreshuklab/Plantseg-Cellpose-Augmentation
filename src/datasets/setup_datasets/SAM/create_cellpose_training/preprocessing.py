import os
import argparse
import skimage.io
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
                files.append((raw_file, label_file))
    return files

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--label_dir', type=str)
    parser.add_argument('--raw_dir', type=str)
    parser.add_argument('--dst_dir', type=str)
    parser.add_argument('--max_slice', type=int, default= -1 )
    config = parser.parse_args()

    # Assert all exist
    assert os.path.isdir(config.label_dir), "label dir must exist"
    assert os.path.isdir(config.raw_dir), "Raw dir must exist"
    assert os.path.isdir(config.dst_dir), "Dst dir must exist"
    
    # find matching names in label and raw path
    matched_files = find_matching_files(config.raw_dir, config.label_dir, file_ext='tif')

    # Go through files in label
    for raw_file,label_file in matched_files:        
        ## Open the file
        raw = skimage.io.imread(os.path.join(config.raw_dir, raw_file))
        label = skimage.io.imread(os.path.join(config.label_dir, label_file))
        
        ## Continue if all label is empty (bg == 1)
        if np.all(label==1): continue
        ## Convert background to 0 
        if label.min() == 1:
            label[label==1] = 0
            label[label==label.max()] = 1
        elif label.min() > 1:
            assert False
        

        ## Loop through slices
        for z_slice in range(len(label)):  
            if z_slice == config.max_slice: break
            #if np.all(label[z_slice] == 0): continue 
            ### Name slice
            new_raw_file = getFileName(raw_file) + '_slice'+str(z_slice).zfill(3) + '_raw.tif'
            new_label_file = getFileName(label_file) + '_slice'+str(z_slice).zfill(3) + '_label.tif'
            ### Save slice in dst
            skimage.io.imsave(os.path.join(config.dst_dir, new_raw_file), raw[z_slice: z_slice+1])
            skimage.io.imsave(os.path.join(config.dst_dir, new_label_file), label[z_slice: z_slice+1])

    






