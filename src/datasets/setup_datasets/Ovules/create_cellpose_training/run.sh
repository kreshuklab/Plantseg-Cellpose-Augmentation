#!/bin/bash
# Make conda work
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate jenv

# Setup path var
DATA_DIR="/scratch/ottosson/datasets/Ovules"

ORIGINAL_DIR="${DATA_DIR}/original"
CELLPOSE_TRAINING_DIR="${DATA_DIR}/cellpose_training"

# Preprocessing
## Find matches in label and raw
## Change background in label 1 to 0
## Slice raw and label and save in CELLPOSE_TRAINING_DIR
python preprocessing.py --original_dir $ORIGINAL_DIR --dst_dir $CELLPOSE_TRAINING_DIR --max_slice -1

# Create flows
conda activate cellpose
CUDA_VISIBLE_DEVICES=5 python -m cellpose --train --dir  $CELLPOSE_TRAINING_DIR --pretrained_model None --use_gpu --n_epochs 1 --img_filter raw --mask_filter label

# Postprocessing
## remove '_raw' from the 'flows' files' name
## remove the 'models' folder
python postprocessing.py --dir $CELLPOSE_TRAINING_DIR



