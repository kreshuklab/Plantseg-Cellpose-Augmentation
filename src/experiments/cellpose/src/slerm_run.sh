#!/bin/bash

#SBATCH -A kreshuk
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --mem 512G
#SBATCH -t 12:00:00
#SBATCH -o /scratch/ottosson/investigation/cellpose/logs/log_02.log
#SBATCH -e /scratch/ottosson/investigation/cellpose/logs/err_02.log
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=joel.ottosson@embl.de
#SBATCH -p gpu
#SBATCH --gres=gpu:1

module load cuDNN

/scratch/ottosson/investigation/cellpose/src/run.sh /scratch/ottosson/investigation/cellpose/experiments/exp_210/configs/config_exp.yml

echo "Job finished"
