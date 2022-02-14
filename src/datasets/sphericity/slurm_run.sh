#!/bin/bash

#SBATCH -A kreshuk
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --mem 16G
#SBATCH -t 2:00:00
#SBATCH -o /scratch/ottosson/investigation/cellpose/logs/log_03.log
#SBATCH -e /scratch/ottosson/investigation/cellpose/logs/err_03.log
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=joel.ottosson@embl.de


# Make conda work
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate napari-test
echo "Conda works"
module load cuDNN

python /scratch/ottosson/datasets/src/sphericity/run2.py --node_id 3 --num_nodes 4
echo 'Job Done'