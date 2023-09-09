import os, json
absolute_path = os.path.abspath(__file__)
config_path = os.path.join(os.path.dirname(absolute_path),"data",'default_config.json')

def load_config(file=config_path):
    with open(file,"r") as config_file: 
        return json.load(config_file)
    
def set_config(file=None): 
    with open(config_path,"r") as default_config: 
        default = json.load(default_config)
    if file is None:
        return default
    else: 
        with open(file,"r") as new_config: 
            merge(new_config,default_config)

def merge(new_config,default_config): 
    return 0

config = load_config()
print(config.get("OS_TYPES")[0])