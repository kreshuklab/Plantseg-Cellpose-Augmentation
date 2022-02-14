
# Helpful general functions for running the experiments
import yaml
import os
import h5py


# Load
def load_yml(file_path=None):
    """Load a yaml file safely"""
    with open(file_path, 'r') as stream:
        data = yaml.safe_load(stream)
    return data
def save_yml(save_path=None, data = None):
    """Save a yaml file safely"""
    with open(save_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)
    return

def load_h5(file_path, datasets):
    ims = []
    with h5py.File(file_path, 'r') as f:
        if datasets is None:
            print("Datasets in file: ", f.keys())
            return 
        for dataset in datasets:
            ims.append(f[dataset][:])
    return ims


# Dict methods
def replace_string_from_dict(s, d, left = '<', right = '>'):
    for v, path in dict_leaf_generator(d):
        sub_s = left+ list_to_string(path, sep = '.', start_with_sep=False) + right
        s = s.replace(sub_s, str(v))
    return s

def r_traverse_dict(d, dict_path = None):
    """Recursivly traverses a dict and yileds the leaf values and the path to them"""
    for key, value in d.items():
        current_path = dict_path + [key]
        if isinstance(value, dict):
            yield from r_traverse_dict(value,current_path)
        else:
            yield value, current_path

def dict_leaf_generator(current_dict = None):
    """Generator which returns each leaf element in a dict with the path to that list"""
    if isinstance(current_dict, dict): 
        return r_traverse_dict(current_dict, dict_path= list())
    else:
        return current_dict, []

def get_value_from_dict_path(dictionary, dict_path):
    temp_dict = dictionary
    for key in dict_path:
        try:
            temp_dict = temp_dict[key]
        except (KeyError, TypeError):
            print(f"Dict path {dict_path} could not be found in dictionary")
            return None
    return temp_dict

def set_value_from_dict_path(dictionary,val, dict_path):
    temp_dict = dictionary
    for key in dict_path:
        try:
            temp_dict = temp_dict[key]
        except (KeyError, TypeError):
            print(f"Dict path {dict_path} could not be found in dictionary")
            return None




def list_to_string(l, sep = '.', start_with_sep=False):
    s = sep if start_with_sep else ""
    for item in l:
        s += sep +str(item)
    return s

# Conversion

def exp_id_to_exp_dir(exp_id = None):
    return "exp_"+str(exp_id).zfill(3)

def r_replace_string(current_val, old_val:str, new_val:str): 
    if isinstance(current_val, str):
        return current_val.replace(old_val, new_val)
    if isinstance(current_val, dict):
        for k,v in current_val.items():
            current_val[k] = r_replace_string(v, old_val, new_val)
        return current_val
    if isinstance(current_val, list):
        #Is iterable
        for i,v in enumerate(current_val):
            current_val[i] = r_replace_string(v, old_val, new_val)
        return current_val 
    return current_val

def replace_string(container, old_val:str, new_val:str):
    """Replace a string in a container. Works for dict and iterables"""
    # NOTE: Does not alter sets (they are not mutible)
    return r_replace_string(container, old_val, new_val)


def get_extention(filename):
    return filename.split('.')[-1]

