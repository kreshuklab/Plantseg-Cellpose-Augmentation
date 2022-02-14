#! /bin/bash 
# #! - hash bang statment and says which bash we are going to use.
CONFIG_EXP_PATH=$1;
#
# Make conda work
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate jenv
echo "Conda works"

#CONFIG_SETUP_PATH=$(python /scratch/ottosson/investigation/cellpose/src/setup.py --config_exp $CONFIG_EXP_PATH)
CONFIG_SETUP_PATH=$(python /scratch/ottosson/investigation/cellpose/src/print_config_setup_path.py --config_exp $CONFIG_EXP_PATH)

# TRAIN
#conda activate cellpose
#python /scratch/ottosson/investigation/cellpose/src/train.py --config_setup $CONFIG_SETUP_PATH

# PRED
conda activate cellpose
python /scratch/ottosson/investigation/cellpose/src/predict.py --config_setup $CONFIG_SETUP_PATH

# EVAL
#conda activate jenv
#python /scratch/ottosson/investigation/cellpose/src/evaluate.py --config_setup $CONFIG_SETUP_PATH

