import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def keep_labels(label_array, labels, reset_value = 0):
    # Only save elements of the array which are are in the list.
    # Rest are set to reste_value (0 as default)
    filtered_array = np.where(np.isin(label_array, labels), label_array, reset_value)
    return filtered_array

def get_limits_around_labels(label_array, labels):
    # Return tuple on the form ( (min0, max0), (min1, max1), ...)
    # Where min and max corresponds to the index in dimension 0, 1, ...
    # which encloses the regions in label_array with values in labels
    ###
    # Get coordinates in 'label_array' which are in 'labels'
    coords  = np.where(np.isin(label_array, labels))
    # Return nested tuple where each tuple contains min and max 
    return tuple( (np.min(coord), np.max(coord)) for coord in coords)
    
def get_slices_with_labels(true_seg, predicted_seg, true_labels, predicted_labels, padding = 0):
    assert true_seg.shape == predicted_seg.shape, "Shapes need to be the same of both image inputs"

    true_limits = get_limits_around_labels(true_seg, true_labels)
    predicted_limits = get_limits_around_labels(predicted_seg, predicted_labels)
    # Get extreme limits along each dimension
    limits = tuple((min(t[0],p[0]), max(t[1],p[1])) for t,p in zip(true_limits, predicted_limits))
    padded_limits = tuple((max(0,l[0]-padding), min(true_seg.shape[i],l[1]+padding)) for i,l in enumerate(limits))
    return tuple(slice(pl[0], pl[1]) for pl in padded_limits)


def plot_region_with_labels(true_seg, predicted_seg, true_labels, predicted_labels, padding = 0, only_labels = True, zfactor = 0.5,raw = None):
    # zfactor: float (0,1). zfactor determines which slice in the zdimension is to be used. zfactor = 0, takes the first slice, and 1 takes the last. 
    assert true_seg.ndim == 3, "Must be a 3D image"

    if only_labels:
        true_seg = keep_labels(true_seg, true_labels)
        predicted_seg = keep_labels(predicted_seg, predicted_labels)

    xslice, yslice, zslice = get_slices_with_labels(true_seg, predicted_seg, true_labels, predicted_labels, padding = padding)
    zslice =  int(zfactor*(zslice.start + zslice.stop+1))

    cmap = get_instance_segmentation_cmap(predicted_seg[xslice,yslice,zslice])
    fig, axs = plt.subplots(1,3)
    axs[0].imshow(raw[xslice,yslice,zslice])
    axs[1].imshow(true_seg[xslice,yslice,zslice], cmap = cmap)
    axs[2].imshow(predicted_seg[xslice,yslice,zslice], cmap = cmap)
    return fig, axs

COLORLIST = ["silver",
            "lightcoral",
            "tan",
            "yellowgreen",
            "palegreen",
            "lightskyblue",
            "red",
            "forestgreen", 
            "darkturquoise",
            "cornflowerblue",
            "lavender",
            "thistle",
            "orchid"]

def get_instance_segmentation_cmap(segmentatition):
    seg_min = int(np.min(segmentatition))
    seg_max = int(np.max(segmentatition))
    num_labels = seg_max-seg_min + 1
    num_colors = len(COLORLIST)
    colorlist = [ COLORLIST[ci % num_colors] for ci in range(num_labels)]
    colorlist = ['black'] + colorlist
    return ListedColormap(colorlist)













