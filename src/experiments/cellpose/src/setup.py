


import argparse
import jutil
import os
from os.path import join
from datetime import datetime

ROOT_PATH = "/scratch/ottosson/investigation/cellpose"
DATASET_PATH ="/scratch/ottosson/datasets"
EXPERIMENTS_PATH="/scratch/ottosson/investigation/cellpose/experiments"
DEFAULT_FILES_PATH="/scratch/ottosson/investigation/cellpose/default_files"
SRC_PATH="/scratch/ottosson/investigation/cellpose/src"
#PLANTSEG_MODELS_PATH="/g/kreshuk/joel/.plantseg_models"

MODEL_BASE_NAME = "model_<exp_dir>"
TRAIN_PATH_BASE= DATASET_PATH+"/<trainset>/cellpose_training/train"
VAL_PATH_BASE= DATASET_PATH+"/<trainset>/cellpose_training/val"

RAW_PATH_BASE= DATASET_PATH+"/<predset>/raw"
LABEL_PATH_BASE= DATASET_PATH+"/<predset>/label"


def create_config_setup(config_exp = None):
    # Create config setup
    config_setup = dict()

    now = datetime.now()
    config_setup['start_time'] = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)} {str(now.hour).zfill(2)}:{str(now.month).zfill(2)}"
    # Experiment
    config_setup['exp_id'] = config_exp['exp_id']
    config_setup['exp_dir'] =  jutil.exp_id_to_exp_dir(config_setup['exp_id'])
    config_setup['exp_path'] = join(EXPERIMENTS_PATH, config_setup['exp_dir'])
    # paths
    config_setup['configs_path'] = join(config_setup['exp_path'], 'configs')
    config_setup['predictions_path'] = join(config_setup['exp_path'], 'predictions')
    config_setup['temps_path'] = join(config_setup['exp_path'], 'temps')
    config_setup['results_path'] = join(config_setup['exp_path'], 'results')
    config_setup['models_path'] = join(config_setup['exp_path'], 'models')
    
    config_setup['predsets'] = config_exp['predsets']
    # Set predset paths
    config_setup['rawset_paths'] = dict() 
    config_setup['labelset_paths'] = dict() 
    for predset in config_setup['predsets']:
        config_setup['rawset_paths'][predset] = RAW_PATH_BASE.replace('<predset>',predset)
        config_setup['labelset_paths'][predset] = LABEL_PATH_BASE.replace('<predset>',predset)

    # PREDICTION
    #config_setup['pred'] = dict()
    #config_setup['pred']['pred_path'] = '<pred_path>'
    #config_setup['pred']['model_name'] = MODEL_BASE_NAME.replace('<exp_dir>', config_setup['exp_dir'])
    #config_setup['pred']['save_path'] = '<save_path>'
    #config_setup['pred']['temps_path'] = config_setup['temps_path']

    ## Training
    config_setup['trainset'] = config_exp['trainset']
    config_setup['train'] = dict()
    #config_setup['train']['checkpoint_path'] = join(PLANTSEG_MODELS_PATH, config_setup['pred']['model_name'])
    config_setup['train']['train_path'] = TRAIN_PATH_BASE.replace('<trainset>',config_setup['trainset'])
    config_setup['train']['val_path'] =   VAL_PATH_BASE.replace( '<trainset>', config_setup['trainset'])

    config_setup['transformer'] = config_exp['transformer']
    return config_setup


def main(config_exp = None):
    # Fill config_default_setup
    config_setup = create_config_setup(config_exp = config_exp)
    
    # Make sure it exist structure of experiment
    if not os.path.isdir(config_setup['exp_path']):
        os.mkdir(config_setup['exp_path'])
    if not os.path.isdir(config_setup['configs_path']):
        os.mkdir(config_setup['configs_path'])
    if not os.path.isdir(config_setup['predictions_path']):
        os.mkdir(config_setup['predictions_path'])
    if not os.path.isdir(config_setup['temps_path']):
        os.mkdir(config_setup['temps_path'])
    if not os.path.isdir(config_setup['results_path']):
        os.mkdir(config_setup['results_path'])
    if not os.path.isdir(config_setup['models_path']):
        os.mkdir(config_setup['models_path'])
    for predset in config_setup['predsets']:
        pred_path = join(config_setup['predictions_path'], predset)
        if not os.path.isdir(pred_path):
            os.mkdir(pred_path)


    # Load and fill config_train_default
    config_train = jutil.load_yml(file_path=join(DEFAULT_FILES_PATH, 'config_train_default.yml'))
    #for k,v in config_setup['train'].items():
    #    config_train = jutil.replace_string(config_train, '<'+k+'>',v)
    # Fill config_train wiht transforms?
    config_train['transformer'] = config_setup['transformer']

    ## Load and fill config_pred_default
    #config_pred = jutil.load_yml(file_path=join(DEFAULT_FILES_PATH, 'config_pred_default.yml'))
    #for k,v in config_setup['pred'].items():
    #    config_pred = jutil.replace_string(config_pred, '<'+k+'>',v)

    # save configs
    jutil.save_yml(join(config_setup['configs_path'], 'config_exp.yml'), config_exp)
    jutil.save_yml(join(config_setup['configs_path'], 'config_setup.yml'), config_setup)
    jutil.save_yml(join(config_setup['configs_path'], 'config_train.yml'), config_train)
    #jutil.save_yml(join(config_setup['configs_path'], 'config_pred.yml'), config_pred)

    return config_setup

if __name__ =='__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_exp', type = str, required=True)
    args = parser.parse_args()

    config_exp = jutil.load_yml(file_path=args.config_exp)

    config_setup = main(config_exp = config_exp)
    print(join(config_setup['configs_path'],'config_setup.yml'))


