
import os
import argparse
import jutil
import setup

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_exp')
    args = parser.parse_args()


    config_exp = jutil.load_yml(args.config_exp)
    config_setup_path = os.path.join(setup.EXPERIMENTS_PATH, jutil.exp_id_to_exp_dir(config_exp['exp_id']),
                                     'configs', 'config_setup.yml')
    print(config_setup_path)






