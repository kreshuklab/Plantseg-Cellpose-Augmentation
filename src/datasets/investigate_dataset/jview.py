import skimage.io
import h5py
import numpy as np
import matplotlib.pyplot as plt

def describe(im, name = None):
    if name is not None: print(name)
    print(f"\tdtype: {im.dtype}")
    print(f"\tshape: {im.shape}")
    print(f"\tmin: {im.min()}")
    print(f"\tmean: {im.mean()}")
    print(f"\tmax: {im.max()}")


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
    return ims

def get_extention(file_path):
    return file_path.split('.')[-1]

def read_file(file_path, datasets = None):
    ext = get_extention(file_path)
    if ext == 'tif': return read_tif(file_path)
    if ext == 'h5': return read_h5(file_path, datasets)
    assert False, "Please provide a valid file"


def random_labeling(label, start_label = 1, min_color = 100):
    label=label.astype(int)
    # label to color
    l2c = np.random.randint(min_color, 255, size = (label.max()+1,))
    for l in range(start_label):
        l2c[l] = l
    label_ = np.zeros_like(label)
    for l in np.unique(label):
        if l < start_label: continue
        label_[label==l] = l2c[l]
    return label_


def print_dir(d):
    for k,v in d.items():
        print(k, ": ", v)

