
from ast import Or
import h5py
import os
import skimage.io
import shutil
ORIGINAL_PATH="/scratch/ottosson/datasets/Ovules/original"
RAW_PATH="/scratch/ottosson/datasets/Ovules/raw"
LABEL_PATH="/scratch/ottosson/datasets/Ovules/label"

def get_extention(filename):
    return filename.split('.')[-1]


if __name__ == '__main__':
    if os.path.isdir(RAW_PATH):
        shutil.rmtree(RAW_PATH)
    os.mkdir(RAW_PATH)
    if os.path.isdir(LABEL_PATH):
        shutil.rmtree(LABEL_PATH)
    os.mkdir(LABEL_PATH)

    for sub_dir in os.listdir(ORIGINAL_PATH):
        if not os.path.isdir(os.path.join(ORIGINAL_PATH, sub_dir)): continue
        for filename in os.listdir(os.path.join(ORIGINAL_PATH, sub_dir)):
            if get_extention(filename) != 'h5': continue
            with h5py.File(os.path.join(ORIGINAL_PATH, sub_dir, filename), 'r') as f:
                raw = f['raw'][:]
                label = f['label'][:]
            
            base_name = filename.split('.')[0].replace('_',"")
            skimage.io.imsave(os.path.join(RAW_PATH,base_name+'_raw.tif'), raw)
            skimage.io.imsave(os.path.join(LABEL_PATH,base_name+'_label.tif'), label)




