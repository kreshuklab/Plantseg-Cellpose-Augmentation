#!/bin/bash
# Make conda work
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate 3dunet

DATA_PATH="/scratch/ottosson/datasets/FM"
THIS_PATH=$(dirname "$0")
python ${THIS_PATH}/create_plantseg_training.py --dataset_path $DATA_PATH



