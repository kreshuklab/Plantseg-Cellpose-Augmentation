
import argparse
import os
import shutil

def isTif(filename):
    return filename.split('.')[-1] == 'tif'

def isFlow(filename):
    return filename.split('.')[0].split('_')[-1] == 'flows'



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str)
    config = parser.parse_args()

    # Cut name of flows
    for filename in os.listdir(config.dir):
        if not isTif(filename): continue
        if not isFlow(filename): continue
        new_name = filename.replace('_raw', '')
        # Remove '_raw' from flow names
        os.rename(os.path.join(config.dir,filename),
                  os.path.join(config.dir,new_name))
    
    # Remove the 'models' folder in the training dir
    shutil.rmtree(os.path.join(config.dir, 'models'))



