import os, json
absolute_path = os.path.abspath(__file__)
config_path = os.path.join(os.path.dirname(absolute_path),"data",'default_config.json')
def load_default():
    with open(config_path,"r") as config_file: 
        return json.load(config_file)

def set_config(new_config): 
    global config
    with open(config_path,"r") as default_config: 
        default = json.load(default_config)
    if new_config is None: 
        return default
    new_config = {key: value for key, value in new_config.items() if value is not None}
    res = merge(default,new_config)
    return res


def merge(default_config,new_config): 
    merged_config = default_config.copy()
    for key, value in new_config.items():
        if key in merged_config and isinstance(merged_config[key], dict) and isinstance(value, dict):
            merged_config[key] = merge(merged_config[key], value)
        else:
            merged_config[key] = value
    return merged_config

config = set_config(None)
