import jutil
import argparse
import shutil
import os
from os.path import join
import skimage.io
import numpy as np
from datetime import datetime

def pre_prediction(config_setup, predset):
    # Updata config_pred and save in temps
    config_setup['pred']['save_path'] = join(config_setup['predictions_path'], predset)
    config_setup['pred']['pred_path'] =  config_setup['rawset_paths'][predset]

    config_pred = jutil.load_yml(join(config_setup['configs_path'],'config_pred.yml'))
    for k,v in config_setup['pred'].items():
        config_pred = jutil.replace_string(config_pred, '<'+k+'>',v)
    jutil.save_yml(save_path=join(config_setup['temps_path'],'config_pred.yml'), data = config_pred)

def post_predict(config_setup, predset):
    for filename in os.listdir(join(config_setup['predictions_path'], predset)):
        if jutil.get_extention(filename) == 'h5':
            pred, = jutil.load_h5(join(config_setup['predictions_path'], predset, filename), datasets = ['segmentation'])
            # SOmething about background???
            new_name = filename.split('_')[0] + '_pred.tif'
            """ Checng most frequent to background (not always good...)
            if pred.min() > 1:
                counts = np.bincount(pred.flatten())
                bg = np.argmax(counts)
                pred[pred == bg] = 1
                pred[pred == pred.max()] = bg
            """
            skimage.io.imsave(join(config_setup['predictions_path'], predset, new_name), pred)
        os.remove(join(config_setup['predictions_path'], predset, filename))
    shutil.rmtree(config_setup['temps_path'])
    os.mkdir(config_setup['temps_path'])

if __name__ =='__main__':
    # pars arguem
    parser= argparse.ArgumentParser()
    parser.add_argument('--config_setup')
    args = parser.parse_args()

    config_setup = jutil.load_yml(args.config_setup)

    for predset in config_setup['predsets']:
        now = datetime.now()
        config_setup['pred_' + predset + '_start'] = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)} {str(now.hour).zfill(2)}:{str(now.month).zfill(2)}"   
        pre_prediction(config_setup,predset)
        cmd= f"plantseg --config {join(config_setup['temps_path'],'config_pred.yml')}"
        os.system(cmd)
        post_predict(config_setup, predset)      
        now = datetime.now()
        config_setup['pred_' + predset + '_end'] = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)} {str(now.hour).zfill(2)}:{str(now.month).zfill(2)}"
    
    jutil.save_yml(os.path.join(config_setup['configs_path'],'config_setup.yml'), config_setup)













