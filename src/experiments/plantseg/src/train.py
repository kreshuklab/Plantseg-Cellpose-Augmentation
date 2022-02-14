

import jutil
import argparse
import shutil
import os
from os.path import join
import setup
import time
from datetime import datetime

TRAIN_SCRIPT="/scratch/ottosson/models/pytorch-3dunet/pytorch3dunet/train.py"


if __name__ =='__main__':
    # pars arguem
    parser= argparse.ArgumentParser()
    parser.add_argument('--config_setup')
    args = parser.parse_args()


    config_setup = jutil.load_yml(args.config_setup)
    now = datetime.now()
    config_setup['train_start'] = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)} {str(now.hour).zfill(2)}:{str(now.month).zfill(2)}"
    config_train_path = join(config_setup['configs_path'],'config_train.yml')
    assert os.path.isfile(config_train_path), "Config train_path must exist"
    cmd = f"python {TRAIN_SCRIPT} --config {config_train_path}"
    os.system(cmd)
    now = datetime.now()
    config_setup['train_end'] = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)} {str(now.hour).zfill(2)}:{str(now.month).zfill(2)}"
    jutil.save_yml(os.path.join(config_setup['configs_path'],'config_setup.yml'), config_setup)












