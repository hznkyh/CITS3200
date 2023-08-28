
import os
import sys
# current_directory = os.path.dirname(os.path.abspath(__file__)) 
# target_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'experiments')
target_directory = os.getcwd()
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
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.operation.mtd_operation import MTDOperation
from mtdnetwork.data.constants import ATTACKER_THRESHOLD, OS_TYPES
from mtdnetwork.component.adversary import Adversary
from mtdnetwork.operation.attack_operation import AttackOperation
from mtdnetwork.snapshot.snapshot_checkpoint import SnapshotCheckpoint
from mtdnetwork.statistic.evaluation import Evaluation# create_experiment_snapshots([25, 50, 75, 100])
def sim_params(num_nodes=50,num_endpoints=50,num_subnets=8,num_layers=4,target_layer=4): 
    print("Working")
    test = execute_simulation(start_time=0, finish_time=400, mtd_interval=200, scheme='random',total_nodes=num_nodes,total_endpoints=num_endpoints,total_subnets=num_subnets,total_layers=num_layers)
    # print(test.get_network().get_hosts())
    # for i,host in test.get_network().get_hosts().items():
    #     print(host.ip)
def checks():
    create_experiment_snapshots([25, 50, 75, 100])
    snapshot_checkpoint = SnapshotCheckpoint()
    for size in [25, 50, 75, 100]:
        time_network = TimeNetwork(total_nodes=size)
        adversary = Adversary(network=time_network, attack_threshold=ATTACKER_THRESHOLD)
        snapshot_checkpoint.save_snapshots_by_network_size(time_network, adversary)
        tn, adv = snapshot_checkpoint.load_snapshots_by_network_size(size)
        print(size)
        print("NETWORK")
        print(tn)
        print("ADVERSARY")
        print(adv)
    
