
import os
import skimage.io
from skimage.metrics import variation_of_information, adapted_rand_error, contingency_table
from collections import defaultdict
import pandas as pd
import argparse
import jseg.evaluation
import numpy as np
import logging

# Identifiers
GT_IDENTIFIER = 'gt'
PRED_IDENTIFIER = 'pred'



def evaluate_segmentation(ground_truth, prediction, background_label=1):
    """
    Calculates meassures over the ground truth and prediction.

    Current implemented measures:
    -----------------------------
    variation of information: Measure over and under segmentation of an image.
                             - VoI-over: Meassure of over segmentation
                             - VoI-under: Meassure of under segmentation
                             - VoI: Meassure of total segmentation.
                            
    Adapted Rand Error: Measure quality of segmentation
                        - ar-predcision: Precision according to the Adaptive rand error
                        - ar-recall: Recall of the predicted segmentation according to Adaptive rand error
                        - ar-error: Harmonic mean of the precision and recall.

    parameters:
    -----------
    ground_truth: Image array with int16 values. 
                    0 - Unknown
                    1 - Background
                    >1 - Clusters (cells)
    
    returns:
    --------
        Dictionary mapping name of measure to value.
    
    """
    data = {}
    
    num_gt = len(np.unique(ground_truth))-1
    data['num-cells'] = num_gt 

    ignore_labels = (0,1)

    # Variation of information
    under_seg, over_seg = variation_of_information(ground_truth, prediction, ignore_labels = ignore_labels)
    data['VoI-over'] = over_seg
    data['VoI-under'] = under_seg
    data['VoI'] = over_seg + under_seg

    # addaptive rand error
    are, prec, rec = adapted_rand_error(image_true=ground_truth, image_test=prediction, ignore_labels=ignore_labels)
    data['ar-error'] = are
    data['ar-precision'] = prec
    data['ar-recall'] = rec 


    # Quality
    full_conttable = contingency_table(im_true = ground_truth, im_test= prediction, normalize=False)
    (correct_rate, over_rate, under_rate, miss_rate, divergent_rate) = jseg.evaluation.segmentation_type(full_conttable, num_gt, background_label=background_label)
    data['qual-correct'] = correct_rate
    data['qual-over'] = over_rate
    data['qual-under'] = under_rate
    data['qual-miss'] = miss_rate
    data['qual-divergent'] = divergent_rate   

    # Add your own functions

    return data

def get_extention(file_path):
    return file_path.split('.')[-1]

def get_type(filename):
    """ 
    Return the type of the file.
    
    Given naming convention '<name>_<type>.<ext>' where none of the variables contains '_'.
    """
    return filename.split('.')[0].split('_')[-1]
def get_name(filename):
    """ 
    Return the name of the file.
    
    Given naming convention '<name>_<type>.<ext>' where none of the variables contains '_'.
    """
    return filename.split('.')[0].split('_')[0]

def is_gt(filename):
    """ Is file ground truth or not"""
    return get_type(filename) == GT_IDENTIFIER
def is_pred(filename):
    """ Is file a prediciton or not"""
    return get_type(filename) == PRED_IDENTIFIER
     

def eval_dataset(gt_path, pred_path):
    """ 
    Evaluate the predicted segmentations
    
    Find matching files in 'gt_path' and 'pred_path' which are then compared to create a 
    dictionary with the results.
    Matches are found if they share the same name given that they follow the naming
    convention <name>_<type>.tif. 

    gt_path: Complete path to dictionary with ground truth files.
    pred_path: Complete path to dictionary with ground pred files.
    
    """
    # find matches
    matched_files = []
    for gt_file in os.listdir(gt_path):
        if not is_gt(gt_file): continue
        if not get_extention(gt_file) != 'tif': continue
        for pred_file in os.listdir(pred_path):
            if not is_pred(pred_file):                   continue
            if not get_extention(pred_file) != 'tif':    continue
            if get_name(gt_file) != get_name(pred_file): continue
            matched_files.append((gt_file, pred_file))

    # Log matches
    log_msg = ""
    log_msg += f"Found {len(matched_files)} matches to evaluate:"
    for gt_name, pred_name in matched_files:
        log_msg += f"\n\t{gt_name} <--> {pred_name}"
    logging.info(log_msg) 

    # go through matches
    result = list()
    for label_file, pred_file in matched_files:
        logging.info(f"Evaluating: {get_name(label_file)}")
        gt = skimage.io.imread(os.path.join(gt_path, label_file))
        pred = skimage.io.imread(os.path.join(pred_path, pred_name))

        ## evaluate
        sample_result = evaluate_segmentation(gt, pred)
        sample_result['sample_name'] = get_name(label_file)
        result.append(sample_result)
    return result

import time
if __name__ == '__main__':
    # parse input
    parser = argparse.ArgumentParser(description='Evaluation')
    parser.add_argument('--gt_dir', type=str)
    parser.add_argument('--pred_dir', type = str)
    parser.add_argument('--save_path', type = str)
    parser.add_argument('--gt_identifier', type = str, default='label')
    parser.add_argument('--pred_identifier', type = str, default='pred')
    args = parser.parse_args()

    logging.basicConfig(level= logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    
    # SET GLOBAL CONSTANTS
    GT_IDENTIFIER = args.gt_identifier
    PRED_IDENTIFIER = args.pred_identifier
    
    # get results from directories
    result = eval_dataset(args.gt_dir, args.pred_dir)
    df = pd.json_normalize(result)
    df.to_csv(args.save_path, index = False)
    

