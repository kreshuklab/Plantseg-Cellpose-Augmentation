import os 
import argparse
import jutil
import shutil
from os.path import join
from datetime import datetime

def pre_train(config_setup = None):
    # Check if models is occupied and reset dir
    models = os.listdir(config_setup['models_path'])
    if len(models) > 0:
        print("Already models in models path. Delete: ")
        print(models)
    shutil.rmtree(config_setup['models_path'])
    os.mkdir(config_setup['models_path'])


def post_train(config_setup = None):
    pass

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_setup')
    args = parser.parse_args()

    config_setup = jutil.load_yml(file_path=args.config_setup)
    # Neeeds to save model in other place!!!!!!!!!
    pre_train(config_setup) # delets current model place
    n_epochs = 500
    #n_epochs = 190
    now = datetime.now()
    config_setup['train_start'] = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)} {str(now.hour).zfill(2)}:{str(now.month).zfill(2)}"
    ### Special for continue to train
    #model_path = '/scratch/ottosson/investigation/cellpose/experiments/exp_202/models/cellpose_residual_on_style_on_concatenation_off_exp_202_2022_01_29_19_53_49.510514'
    model_path = 'None'
    cmd = ""
    cmd += f"python -m cellpose --train"
    cmd += f" --dir {config_setup['train']['train_path']}"
    cmd += f" --model_dir {config_setup['exp_path']}"
    cmd += f" --config_train {join(config_setup['configs_path'],'config_train.yml')}"
    cmd += f" --test_dir {config_setup['train']['val_path']}"
    cmd += f" --save_every 10 --pretrained_model {model_path} --use_gpu"
    cmd += f" --n_epochs {n_epochs}"
    cmd += f" --img_filter raw --mask_filter flows"
    os.system(cmd)
    now = datetime.now()
    config_setup['train_end'] = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)} {str(now.hour).zfill(2)}:{str(now.month).zfill(2)}"
    jutil.save_yml(os.path.join(config_setup['configs_path'],'config_setup.yml'), config_setup)
    post_train(config_setup=config_setup)
