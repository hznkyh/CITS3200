
import simpy
import json
from networkx.readwrite import json_graph
# create_experiment_snapshots([25, 50, 75, 100])
from mtdnetwork.statistic.evaluation import Evaluation
from mtdnetwork.snapshot.snapshot_checkpoint import SnapshotCheckpoint
from mtdnetwork.operation.attack_operation import AttackOperation
from mtdnetwork.component.host import Host
from mtdnetwork.component.adversary import Adversary
# from mtdnetwork.data.constants import ATTACKER_THRESHOLD, OS_TYPES
from mtdnetwork.configs import config
from mtdnetwork.operation.mtd_operation import MTDOperation
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.configs import config
from experiments.run import single_mtd_simulation, create_experiment_snapshots, execute_simulation
import matplotlib.pyplot as plt
from itertools import chain, count
import networkx as nx
import pandas as pd
import warnings
import os
import sys
# current_directory = os.path.dirname(os.path.abspath(__file__))
# target_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'experiments')
# target_directory = os.getcwd()
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the "s" directory
target_directory = os.path.join(current_script_dir, "..", "backend")
if not os.path.exists(target_directory + '/experimental_data'):
    os.makedirs(target_directory + '/experimental_data')
    os.makedirs(target_directory + '/experimental_data/plots')
    os.makedirs(target_directory + '/experimental_data/results')
sys.path.append(target_directory.replace('experiments', ''))
# print(current_directory)
print(target_directory)
warnings.filterwarnings("ignore")
plt.set_loglevel('WARNING')


class GraphEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Host):
            return obj.toJson()
        return json.JSONEncoder.default(self, obj)


def sim_params(num_nodes=50, num_endpoints=50, num_subnets=8, num_layers=4, target_layer=4):
    print("Working")
    test = execute_sim(start_time=0, finish_time=200, mtd_interval=20, scheme='random', total_nodes=num_nodes,
                       total_endpoints=num_endpoints, total_subnets=num_subnets, total_layers=num_layers)
    return test
    # print(test.get_network().get_hosts())
    # for i,host in test.get_network().get_hosts().items():
    #     print(host.ip)


def checks():
    create_experiment_snapshots([25, 50, 75, 100])
    snapshot_checkpoint = SnapshotCheckpoint()
    for size in [25, 50, 75, 100]:
        time_network = TimeNetwork(total_nodes=size)
        adversary = Adversary(network=time_network,
                              attack_threshold=config.get("ATTACKER_THRESHOLD"))
        snapshot_checkpoint.save_snapshots_by_network_size(
            time_network, adversary)
        tn, adv = snapshot_checkpoint.load_snapshots_by_network_size(size)
        print(size)
        print("NETWORK")
        print(tn)
        print("ADVERSARY")
        print(adv)


def get_time(event):
    print('Called at ', event.env.now)


def get_results(time_network, env, start_time, finish_time, res):
    for i in range(start_time, finish_time+1, 5):
        yield env.timeout(i-env.now)
        print("GRAPH STATE AT " + str(i))
        # print(time_network.get_host(1).toJson())
        # print(json_graph.node_link_data(time_network.get_graph(),attrs={"host":"toJson"}))
        # res.append(json_graph.node_link_data(
        #     time_network.get_graph(), attrs={"host": "toJson"}))
        res.append(serialize_graph(time_network.get_graph()))
        # print(json.dumps(time_network.get_graph(),default=json_graph.node_link_data))
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
    # TODO Remove test vars
    total_nodes = 16
    new_network = True

    env = simpy.Environment()
    end_event = env.event()
    print("env is ")
    print(env)
    snapshot_checkpoint = SnapshotCheckpoint(env=env, checkpoints=checkpoints)
    time_network = None
    adversary = None
    res = list()
    if start_time > 0:
        try:
            time_network, adversary = snapshot_checkpoint.load_snapshots_by_time(
                start_time)
        except FileNotFoundError:
            print('No timestamp-based snapshots available! Set start_time = 0 !')
            return
    elif not new_network:
        try:
            time_network, adversary = snapshot_checkpoint.load_snapshots_by_network_size(
                total_nodes)
        except FileNotFoundError:
            print('set new_network=True')
    else:
        time_network = TimeNetwork(total_nodes=total_nodes, total_endpoints=total_endpoints,
                                   total_subnets=total_subnets, total_layers=total_layers,
                                   target_layer=target_layer, total_database=total_database,
                                   terminate_compromise_ratio=terminate_compromise_ratio)
        adversary = Adversary(network=time_network,
                              attack_threshold=config.get("ATTACKER_THRESHOLD"))
        # snapshot_checkpoint.save_initialised(time_network, adversary)
        snapshot_checkpoint.save_snapshots_by_network_size(
            time_network, adversary)

    # start attack
    attack_operation = AttackOperation(
        env=env, end_event=end_event, adversary=adversary, proceed_time=0)
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
    env.process(get_results(time_network=time_network, env=env,
                start_time=start_time, finish_time=finish_time, res=res))
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
    return res


#!: OLd code
def create_sim(
    env: simpy.Environment,
    res: list,
    start_time=0,
    finish_time=None,
    scheme='random',
    mtd_interval=None,
    custom_strategies=None,
    checkpoints=None,
    total_nodes=50,
    total_endpoints=5,
    total_subnets=8,
    total_layers=4,
    target_layer=4,
    total_database=2,
    terminate_compromise_ratio=0.8,
    new_network=False
):
    '''The `create_sim` function creates a simulation environment for a network attack and defense
    scenario, with options for different attack and defense strategies, network parameters, and
    checkpointing.
    
    Parameters
    ----------
    env : simpy.Environment
        The simpy environment in which the simulation will run.
    start_time, optional
        The start time at which the simulation should begin. If set to a value greater than 0, the
    simulation will load snapshots of the network and adversary at that time. If set to 0, the
    simulation will start with a new network.
    finish_time
        The time at which the simulation will finish. If not specified, the simulation will run
    indefinitely.
    scheme, optional
        The `scheme` parameter determines the MTD (Moving Target Defense) scheme to be used. It can take
    the following values:
    mtd_interval
        The `mtd_interval` parameter is the interval at which the MTD (Moving Target Defense) operation is
    triggered. It determines how often the MTD strategies are applied to the network to mitigate
    attacks.
    custom_strategies
        The `custom_strategies` parameter is a list that allows you to specify custom MTD strategies to be
    used in the simulation. These strategies can be defined as functions and will be executed during the
    MTD operation. Each strategy function should take the following parameters:
    checkpoints
        A list of time points at which to save snapshots of the network and adversary state.
    total_nodes, optional
        The total number of nodes in the network.
    total_endpoints, optional
        The parameter "total_endpoints" represents the total number of endpoints in the simulated network.
    Endpoints are devices or systems that are connected to the network and can be potential targets for
    attacks.
    total_subnets, optional
        The parameter "total_subnets" represents the total number of subnets in the network. A subnet is a
    portion of a network that shares a common network address. It is used to divide a large network into
    smaller, more manageable parts.
    total_layers, optional
        The parameter "total_layers" represents the total number of layers in the network. Each layer
    represents a level of hierarchy in the network topology. For example, in a hierarchical network
    architecture, there may be multiple layers of switches or routers, with each layer providing
    connectivity to a subset of nodes in the network
    target_layer, optional
        The parameter "target_layer" specifies the layer in the network where the attack is targeted.
    total_database, optional
        The parameter "total_database" represents the total number of databases in the simulation.
    terminate_compromise_ratio
        The `terminate_compromise_ratio` parameter is used to determine the threshold at which the attack
    is considered successful. It represents the ratio of compromised nodes in the network that will
    trigger the termination of the attack. For example, if `terminate_compromise_ratio` is set to 0.8,
    the
    new_network, optional
        A boolean value indicating whether to create a new network or load an existing one. If set to True,
    a new network will be created. If set to False, an existing network will be loaded if available,
    otherwise an error message will be printed.
    
    Returns
    -------
        The function `create_sim` returns two values: `evaluation` and `res`.
    
    '''
    print("running with config ",config)
    end_event = env.event()
    snapshot_checkpoint = SnapshotCheckpoint(env=env, checkpoints=[0.5,1,1.5])
    time_network = None
    adversary = None
    if start_time > 0:
        try:
            time_network, adversary = snapshot_checkpoint.load_snapshots_by_time(
                start_time)
        except FileNotFoundError:
            print('No timestamp-based snapshots available! Set start_time = 0 !')
            return
    elif not new_network:
        try:
            time_network, adversary = snapshot_checkpoint.load_snapshots_by_network_size(
                total_nodes)
        except FileNotFoundError:
            print('set new_network=True')
    else:
        time_network = TimeNetwork(total_nodes=total_nodes, total_endpoints=total_endpoints,
                                   total_subnets=total_subnets, total_layers=total_layers,
                                   target_layer=target_layer, total_database=total_database,
                                   terminate_compromise_ratio=terminate_compromise_ratio)
        adversary = Adversary(network=time_network,
                              attack_threshold=config.get("ATTACKER_THRESHOLD"))
        # snapshot_checkpoint.save_to_array(time_network, adversary, res)


    # start attack
    attack_operation = AttackOperation(
        env=env, end_event=end_event, adversary=adversary, proceed_time=0)
    attack_operation.proceed_attack()

    # start mtd
    if scheme != 'None':
        mtd_operation = MTDOperation(env=env, end_event=end_event, network=time_network, scheme=scheme,
                                     attack_operation=attack_operation, proceed_time=0,
                                     mtd_trigger_interval=mtd_interval, custom_strategies=custom_strategies)
        mtd_operation.proceed_mtd()

    # save snapshot by time
    print("proceed save checkpoints",checkpoints)
    if checkpoints is not None:
        snapshot_checkpoint.proceed_save(time_network, adversary,res)

    # Evaluate the simulation
    evaluation = Evaluation(network=time_network, adversary=adversary)

    return evaluation

def create_sim_test(
    env: simpy.Environment,
    res: list,
    start_time=0,
    finish_time=None,
    checkpoints=None,
    new_network=False,
    scheme='random',
    mtd_interval=None,
    custom_strategies=None,
    total_nodes=50,
    total_endpoints=5,
    total_subnets=8,
    total_layers=4,
    target_layer=4,
    total_database=2,
    terminate_compromise_ratio=0.8
):
    '''The `create_sim` function creates a simulation environment for a network attack and defense
    scenario, with options for different attack and defense strategies, network parameters, and
    checkpointing.
    
    Parameters
    ----------
    env : simpy.Environment
        The simpy environment in which the simulation will run.
    start_time, optional
        The start time at which the simulation should begin. If set to a value greater than 0, the
    simulation will load snapshots of the network and adversary at that time. If set to 0, the
    simulation will start with a new network.
    finish_time
        The time at which the simulation will finish. If not specified, the simulation will run
    indefinitely.
    scheme, optional
        The `scheme` parameter determines the MTD (Moving Target Defense) scheme to be used. It can take
    the following values:
    mtd_interval
        The `mtd_interval` parameter is the interval at which the MTD (Moving Target Defense) operation is
    triggered. It determines how often the MTD strategies are applied to the network to mitigate
    attacks.
    custom_strategies
        The `custom_strategies` parameter is a list that allows you to specify custom MTD strategies to be
    used in the simulation. These strategies can be defined as functions and will be executed during the
    MTD operation. Each strategy function should take the following parameters:
    checkpoints
        A list of time points at which to save snapshots of the network and adversary state.
    total_nodes, optional
        The total number of nodes in the network.
    total_endpoints, optional
        The parameter "total_endpoints" represents the total number of endpoints in the simulated network.
    Endpoints are devices or systems that are connected to the network and can be potential targets for
    attacks.
    total_subnets, optional
        The parameter "total_subnets" represents the total number of subnets in the network. A subnet is a
    portion of a network that shares a common network address. It is used to divide a large network into
    smaller, more manageable parts.
    total_layers, optional
        The parameter "total_layers" represents the total number of layers in the network. Each layer
    represents a level of hierarchy in the network topology. For example, in a hierarchical network
    architecture, there may be multiple layers of switches or routers, with each layer providing
    connectivity to a subset of nodes in the network
    target_layer, optional
        The parameter "target_layer" specifies the layer in the network where the attack is targeted.
    total_database, optional
        The parameter "total_database" represents the total number of databases in the simulation.
    terminate_compromise_ratio
        The `terminate_compromise_ratio` parameter is used to determine the threshold at which the attack
    is considered successful. It represents the ratio of compromised nodes in the network that will
    trigger the termination of the attack. For example, if `terminate_compromise_ratio` is set to 0.8,
    the
    new_network, optional
        A boolean value indicating whether to create a new network or load an existing one. If set to True,
    a new network will be created. If set to False, an existing network will be loaded if available,
    otherwise an error message will be printed.
    
    Returns
    -------
        The function `create_sim` returns two values: `evaluation` and `res`.
    
    '''
    print("running with config ",config)
    end_event = env.event()
    snapshot_checkpoint = SnapshotCheckpoint(env=env, checkpoints=checkpoints)
    time_network = None
    adversary = None
    if start_time > 0:
        try:
            time_network, adversary = snapshot_checkpoint.load_snapshots_by_time(
                start_time)
        except FileNotFoundError:
            print('No timestamp-based snapshots available! Set start_time = 0 !')
            return
    elif not new_network:
        try:
            time_network, adversary = snapshot_checkpoint.load_snapshots_by_network_size(
                total_nodes)
        except FileNotFoundError:
            print('set new_network=True')
    else:
        time_network = TimeNetwork(total_nodes=total_nodes, total_endpoints=total_endpoints,
                                   total_subnets=total_subnets, total_layers=total_layers,
                                   target_layer=target_layer, total_database=total_database,
                                   terminate_compromise_ratio=terminate_compromise_ratio)
        print(config)
        adversary = Adversary(network=time_network,
                              attack_threshold=config.get("ATTACKER_THRESHOLD"))
        # snapshot_checkpoint.save_to_array(time_network, adversary, res)


    # start attack
    attack_operation = AttackOperation(
        env=env, end_event=end_event, adversary=adversary, proceed_time=0)
    attack_operation.proceed_attack()

    # start mtd
    if scheme != 'None':
        mtd_operation = MTDOperation(env=env, end_event=end_event, network=time_network, scheme=scheme,
                                     attack_operation=attack_operation, proceed_time=0,
                                     mtd_trigger_interval=mtd_interval, custom_strategies=custom_strategies)
        mtd_operation.proceed_mtd()

    # save snapshot by time
    print("proceed save checkpoints",checkpoints)
    if checkpoints is not None:
        snapshot_checkpoint.proceed_save(time_network, adversary,res)

    # Evaluate the simulation
    evaluation = Evaluation(network=time_network, adversary=adversary)
    
    # start simulation
    if finish_time is not None:
        env.run(until=(finish_time - start_time))
    else:
        env.run(until=end_event)
    evaluation = Evaluation(network=time_network, adversary=adversary)

    return evaluation

def serialize_graph(G:nx.Graph, attrs=None):
    """Returns data in node-link format that is suitable for JSON serialization
    and use in Javascript documents.

    Parameters
    ----------
    G : NetworkX graph

    attrs : dict
        A dictionary that contains five keys 'source', 'target', 'name',
        'key' and 'link'.  The corresponding values provide the attribute
        names for storing NetworkX-internal graph data.  The values should
        be unique.  Default value::

            dict(source='source', target='target', name='id',
                 key='key', link='links')

        If some user-defined graph data use these attribute names as data keys,
        they may be silently dropped.

    Returns
    -------
    data : dict
       A dictionary with node-link formatted data.

    Raises
    ------
    NetworkXError
        If values in attrs are not unique.

    Examples
    --------

    Notes
    -----
    Graph, node, and link attributes are stored in this format.  Note that
    attribute keys will be converted to strings in order to comply with JSON.
    """
    _attrs = dict(source="source", target="target", name="id", key="key", link="links")
    multigraph = G.is_multigraph()
    # Allow 'attrs' to keep default values.
    if attrs is None:
        attrs = _attrs
    else:
        attrs.update({k: v for (k, v) in _attrs.items() if k not in attrs})
    name = attrs["name"]
    source = attrs["source"]
    print(source)
    target = attrs["target"]
    links = attrs["link"]
    # Allow 'key' to be omitted from attrs if the graph is not a multigraph.
    key = None if not multigraph else attrs["key"]
    if len({source, target, key}) < 3:
        raise nx.NetworkXError("Attribute names are not unique.")
    data = {
        "directed": G.is_directed(),
        "multigraph": multigraph,
        "graph": G.graph,
        "nodes": [serialize_class(G,n,name)  for n in G],
        # "nodes": [dict(chain(G.nodes[n].items(), [(name, n)])) for n in G],
    }
        
    if multigraph:
        data[links] = [
            dict(chain(d.items(), [(source, u), (target, v), (key, k)]))
            for u, v, k, d in G.edges(keys=True, data=True)
        ]
    else:            
        data[links] = [
            dict(chain(d.items(), [(source, u), (target, v)]))
            for u, v, d in G.edges(data=True)
        ]
    return data
    # return data

def serialize_class(G,n,name):
    node = dict(chain(G.nodes[n].items(), [(name, n)]))
    if ('host' in node):
        node['host'] = node['host'].toJson()
    return node

