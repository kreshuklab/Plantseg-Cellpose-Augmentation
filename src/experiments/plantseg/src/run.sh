#! /bin/bash 
# #! - hash bang statment and says which bash we are going to use.
CONFIG_EXP_PATH=$1;

export PYTHONPATH=/scratch/ottosson/models/pytorch-3dunet:$PYTHONPATH

# Make conda work
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate jenv

CONFIG_SETUP_PATH=$(python setup.py --config_exp $CONFIG_EXP_PATH)
#CONFIG_SETUP_PATH=$(python print_config_setup_path.py --config_exp $CONFIG_EXP_PATH)
#
# TRAIN
conda activate 3dunet
python train.py --config_setup $CONFIG_SETUP_PATH

# PRED
conda activate plant-seg
python predict.py --config_setup $CONFIG_SETUP_PATH

# EVAL
conda activate jenv
python evaluate.py --config_setup $CONFIG_SETUP_PATH

