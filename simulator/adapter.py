
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__)) 
target_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'experiments')
if not os.path.exists(target_directory + '/experimental_data'):
    os.makedirs(target_directory + '/experimental_data')
    os.makedirs(target_directory + '/experimental_data/plots')
    os.makedirs(target_directory + '/experimental_data/results')
sys.path.append(target_directory.replace('experiments', ''))
# print(current_directory)
print(target_directory)
import warnings
import pandas as pd
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.set_loglevel('WARNING')
from experiments.run import single_mtd_simulation, create_experiment_snapshots, execute_simulation
create_experiment_snapshots([25, 50, 75, 100])
num_nodes = 50
num_endpoints = 50
num_subnets = 8
num_layers = 4
target_layer = 4
test = execute_simulation(total_nodes=num_nodes,total_endpoints=num_endpoints,total_subnets=num_subnets,total_layers=num_layers)
test.visualise_attack_operation()
test.draw_network()
test.draw_compromised()