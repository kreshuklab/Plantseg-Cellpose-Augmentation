#!/bin/bash
# Make conda work
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate jenv

# Setup path var
DATA_PATH="/scratch/ottosson/datasets/SAM"

PLANTSEG_PATH="${DATA_PATH}/plantseg_training"
# Go through train and val folders in plantseg and exctract raw and label
# save them as .tif in coresponding folders
python create_raw_label_from_plantseg.py --plantseg_path $PLANTSEG_PATH --dataset_path $DATA_PATH


