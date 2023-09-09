import os, json, tempfile
absolute_path = os.path.abspath(__file__)
config_path = os.path.join(os.path.dirname(absolute_path),"data",'default_config.json')

def load_default():
    with open(config_path,"r") as config_file: 
        return json.load(config_file)

def test_file(): 
    temp = tempfile.TemporaryFile()
    try: 
        temp.write(b'{"MTD_PRIORITY": {"CompleteTopologyShuffle": 1, "HostTopologyShuffle": 2, "IPShuffle": 3, "OSDiversity": 5, "PortShuffle": 4, "ServiceDiversity": 7, "UserShuffle": 6 } }')
        temp.seek(0)
        json_data = temp.read().decode()
        print(json.loads(json_data).get("MTD_PRIORITY"))
    finally: 
        temp.close() 

    # print("Json string",json.load(json_data.decode()))
def set_config(file=None): 
    temp = tempfile.TemporaryFile()
    try: 
        temp.write(b'{"MTD_PRIORITY": {"CompleteTopologyShuffle": 1, "HostTopologyShuffle": 4, "IPShuffle": 3, "OSDiversity": 2, "PortShuffle": 5, "ServiceDiversity": 7, "UserShuffle": 6 } }')
        temp.seek(0)
        json_data = json.loads(temp.read().decode())
        print(json_data)
    finally: 
        temp.close() 
    with open(config_path,"r") as default_config: 
        default = json.load(default_config)

    res = merge(default,json_data)
    return res
    # if file is None:
    #     return load_default()
    # else: 
    #     # with open(file,"r") as new_config: 
    #     merge(json_data,default_config)

def merge(default_config,new_config): 
    merged_config = default_config.copy()
    for key, value in new_config.items():
        if key in merged_config and isinstance(merged_config[key], dict) and isinstance(value, dict):
            merged_config[key] = merge(merged_config[key], value)
        else:
            print(key, " is ", merged_config[key])
            merged_config[key] = value
            print("Changed",key, " to ", value)
    print("MERGED IS ",merged_config)
    return merged_config

test_file()
config = set_config()
print(load_default().get("MTD_PRIORITY"))
print(config.get("MTD_PRIORITY"))