

import numpy as np
from skimage import draw


OVERLAPPING_CIRCLE_TYPES = ("over-segmentation",
                            "under-segmentation",
                            "single-correct-segmentation",
                            "double-correct-segmentation",
                            "single-switched-segmentation",
                            "double-semi-correct-segmentation",
                            "extra-segmentation",
                            "missed-segmentation",
                            "divergent-segmentation",
                            )

def overlapping_circles(segmentation_type:str= 'over-segmentation', background_label:int= 0,
                        shape:tuple= None, radius:float=None, offset:int=None,
                        extend_axis:int= None, label_shift = False):
    """
    Returns a tuple of two numpy.ndarrays. The arrays can be seen as images'.
    The images have some number of disks depending on the 'segmentation_type'-input.
    The disks can either have the same label (same value) or different.
    """


    # Handle segmentation type
    assert segmentation_type in OVERLAPPING_CIRCLE_TYPES, f"Segmentation_type needs to be one of: {OVERLAPPING_CIRCLE_TYPES}"

    # Handle shape input
    if not shape:
        shape = tuple((100,100))
    assert len(shape) == 2, "Shape must be of lenght 2"
    # Handle radius input
    if not radius:
        radius = min(shape)/4.
    # Handle offset input    
    if not offset:
        offset = int(2/3*radius)

    # Create images
    label = background_label*np.ones(shape, dtype="uint16")
    segmentaiton = background_label*np.ones(shape, dtype="uint16")
    
    # Abbriviations:
    #   o - over
    #   u - under
    #   d - disk
    #   r - row
    #   c - column
    center = [int(dim_len/2) for dim_len in shape]
    odr, odc = draw.disk((center[0],center[1]-offset), radius, shape = shape)
    udr, udc = draw.disk((center[0],center[1]+offset), radius, shape = shape)
    odr_s, odc_s = draw.disk((center[0],center[1]-offset//2), radius/2, shape = shape)
    udr_s, udc_s = draw.disk((center[0],center[1]+offset//2), radius/2, shape = shape)
    # Fill in circles depending on segmentation type
    if segmentation_type == "over-segmentation":
        label[odr, odc] = background_label+1
        label[udr, udc] = background_label+1
        segmentaiton[odr, odc] = background_label+1
        segmentaiton[udr, udc] = background_label+2
    elif segmentation_type == "under-segmentation":
        label[odr, odc] = background_label+1
        label[udr, udc] = background_label+2
        segmentaiton[odr, odc] = background_label+1
        segmentaiton[udr, udc] = background_label+1
    elif segmentation_type == "single-correct-segmentation":
        label[odr, odc] = background_label+1
        segmentaiton[odr, odc] = background_label+1
    elif segmentation_type == "double-correct-segmentation":
        label[odr, odc] = background_label+1
        label[udr, udc] = background_label+2
        segmentaiton[odr, odc] = background_label+1
        segmentaiton[udr, udc] = background_label+2
    elif segmentation_type == "double-semi-correct-segmentation":
        label[odr, odc] = background_label+1
        label[udr, udc] = background_label+2
        segmentaiton[udr, udc] = background_label+1
        segmentaiton[odr, odc] = background_label+2
    elif segmentation_type == "single-switched-segmentation":
        label[odr, odc] = background_label+1
        segmentaiton[udr, udc] = background_label+1
    elif segmentation_type == "extra-segmentation":
        label[odr, odc] = background_label+1
        segmentaiton[odr, odc] = background_label+1
        segmentaiton[udr, udc] = background_label+2
    elif segmentation_type == "missed-segmentation":
        label[odr, odc] = background_label+1
        label[udr, udc] = background_label+2
        segmentaiton[udr, udc] = background_label+2
    elif segmentation_type == "divergent-segmentation":
        label[odr, odc] = background_label+1
        label[udr_s, udc_s] = background_label+2
        segmentaiton[udr, udc] = background_label+1
        segmentaiton[odr_s, odc_s] = background_label+2
    # Extend dimension
    if extend_axis is not None:
        label = np.expand_dims(label, axis = extend_axis)
        segmentaiton = np.expand_dims(segmentaiton, axis = extend_axis)

    if label_shift:
        segmentaiton = 1000*segmentaiton

    return label, segmentaiton









