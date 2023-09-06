import sys
import os
from pathlib import Path
import threading
import json

# Get the absolute path of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the "s" directory
s_directory = os.path.join(current_script_dir, "..", "simulator")
sys.path.append(s_directory)
from adapter import *
# a= sim_params()
# # print(a[0])
# b = json.dumps(a)
# print(b)
def get_sim_json(): 
    # Add the "s" directory to the Python path
    a= sim_params()
    # print(a[0])
    b = json.dumps(a)
    return b
    # checks()
print(get_sim_json())
# import simpy
# env = simpy.Environment()
# simulation_thread = None
# # evaluation , res = run_sim(env, start_time=0, finish_time= 4)
# evaluation , res = create_sim(env, start_time=0, finish_time= 4)
# # for i in res: 
# #     print(i)
# simulation_thread = threading.Thread(target=env.run, args=(([2])))
# simulation_thread.start()
# simulation_thread.join()
# print(simulation_thread.is_alive())

# print(res, evaluation.get_network().graph.number_of_nodes(), sep='\n')