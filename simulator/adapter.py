
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
from mtdnetwork.component.host import Host
from mtdnetwork.operation.attack_operation import AttackOperation
from mtdnetwork.snapshot.snapshot_checkpoint import SnapshotCheckpoint
from mtdnetwork.statistic.evaluation import Evaluation# create_experiment_snapshots([25, 50, 75, 100])
from networkx.readwrite import json_graph
import json
import simpy

class GraphEncoder(json.JSONEncoder): 
    def default(self,obj): 
        if isinstance(obj,Host):
            return obj.toJson()
        return json.JSONEncoder.default(self,obj)

def sim_params(num_nodes=50,num_endpoints=50,num_subnets=8,num_layers=4,target_layer=4): 
    print("Working")
    test = execute_sim(start_time=0, finish_time=200, mtd_interval=20, scheme='random',total_nodes=num_nodes,total_endpoints=num_endpoints,total_subnets=num_subnets,total_layers=num_layers)
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
    
def get_time(event):
    print('Called at ',event.env.now) 

def get_results(time_network,env,start_time,finish_time): 
    for i in range(start_time,finish_time+1,5): 
        yield env.timeout(i-env.now)
        print("GRAPH STATE AT " + str(i))
        # print(time_network.get_host(1).toJson())
        print(json_graph.node_link_data(time_network.get_graph(),attrs={"host":"toJson"}))
        print(json.dumps(time_network.get_graph(),default=json_graph.node_link_data))
        # print(time_network.get_hosts())


def execute_sim(start_time=0, finish_time=None, scheme='random', mtd_interval=None, custom_strategies=None,
                       checkpoints=None, total_nodes=50, total_endpoints=5, total_subnets=8, total_layers=4,
                       target_layer=4, total_database=2, terminate_compromise_ratio=0.8, new_network=False):
    """

    :param start_time: the time to start the simulation, need to load timestamp-based snapshots if set start_time > 0
    :param finish_time: the time to finish the simulation. Set to None will run the simulation until
    the network reached compromised threshold (compromise ratio > 0.9)
    :param scheme: random, simultaneous, alternative, single, None
    :param mtd_interval: the time interval to trigger an MTD(s)
    :param custom_strategies: used for executing alternative scheme or single mtd strategy.
    :param checkpoints: a list of time value to save snapshots as the simulation runs.
    :param total_nodes: the number of nodes in the network (network size)
    :param total_endpoints: the number of exposed nodes
    :param total_subnets: the number of subnets (total_nodes - total_endpoints) / (total_subnets - 1) > 2
    :param total_layers: the number of layers in the network
    :param target_layer: the target layer in the network (for targetted attack scenario only)
    :param total_database: the number of database nodes used for computing DAP algorithm
    :param terminate_compromise_ratio: terminate the simulation if reached compromise ratio
    :param new_network: True: create new snapshots based on network size, False: load snapshots based on network size
    """
    # initialise the simulation
    env = simpy.Environment()
    end_event = env.event()
    print("env is ")
    print(env)
    snapshot_checkpoint = SnapshotCheckpoint(env=env, checkpoints=checkpoints)
    time_network = None
    adversary = None

    if start_time > 0:
        try:
            time_network, adversary = snapshot_checkpoint.load_snapshots_by_time(start_time)
        except FileNotFoundError:
            print('No timestamp-based snapshots available! Set start_time = 0 !')
            return
    elif not new_network:
        try:
            time_network, adversary = snapshot_checkpoint.load_snapshots_by_network_size(total_nodes)
        except FileNotFoundError:
            print('set new_network=True')
    else:
        time_network = TimeNetwork(total_nodes=total_nodes, total_endpoints=total_endpoints,
                                   total_subnets=total_subnets, total_layers=total_layers,
                                   target_layer=target_layer, total_database=total_database,
                                   terminate_compromise_ratio=terminate_compromise_ratio)
        adversary = Adversary(network=time_network, attack_threshold=ATTACKER_THRESHOLD)
        # snapshot_checkpoint.save_initialised(time_network, adversary)
        snapshot_checkpoint.save_snapshots_by_network_size(time_network, adversary)

    # start attack
    attack_operation = AttackOperation(env=env, end_event=end_event, adversary=adversary, proceed_time=0)
    attack_operation.proceed_attack()

    # start mtd
    if scheme != 'None':
        mtd_operation = MTDOperation(env=env, end_event=end_event, network=time_network, scheme=scheme,
                                     attack_operation=attack_operation, proceed_time=0,
                                     mtd_trigger_interval=mtd_interval, custom_strategies=custom_strategies)
        mtd_operation.proceed_mtd()

    # save snapshot by time
    if checkpoints is not None:
        snapshot_checkpoint.proceed_save(time_network, adversary)
    env.process(get_results(time_network=time_network,env=env,start_time=start_time,finish_time=finish_time)) 
    # start simulation
    if finish_time is not None:
        env.run(until=(finish_time - start_time))
        print("ENDED1")
    else:
        env.run(until=end_event)
        print("ENDED2")
    evaluation = Evaluation(network=time_network, adversary=adversary)

    # sim_item = scheme
    # if scheme == 'single':
    #     sim_item = custom_strategies().get_name()
    # elif scheme == 'None':
    #     sim_item = 'NoMTD'
    # time_network.get_mtd_stats().save_record(sim_time=mtd_interval, scheme=sim_item)
    # adversary.get_attack_stats().save_record(sim_time=mtd_interval, scheme=sim_item)

    return evaluation