import os, json
absolute_path = os.path.abspath(__file__)
config_path = os.path.join(os.path.dirname(absolute_path),"data",'default_config.json')

def load_default():
    with open(config_path,"r") as config_file: 
        return json.load(config_file)
    
def set_config(file=None): 
    with open(config_path,"r") as default_config: 
        default = json.load(default_config)
    if file is None:
        return load_default()
    else: 
        with open(file,"r") as new_config: 
            merge(new_config,default_config)

def merge(new_config,default_config): 
    merged_config = default_config.copy()
    for key, value in new_config.items():
        if key in merged_config and isinstance(merged_config[key], dict) and isinstance(value, dict):
            merged_config[key] = merge(merged_config[key], value)
        else:
            merged_config[key] = value
    return merged_config

config = set_config()
print(config.get("OS_TYPES")[0])