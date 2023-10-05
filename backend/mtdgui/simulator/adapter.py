import logging
import simpy
import json
from networkx.readwrite import json_graph

# create_experiment_snapshots([25, 50, 75, 100])
from simulator.mtdnetwork.statistic.evaluation import Evaluation
from simulator.mtdnetwork.snapshot.snapshot_checkpoint import SnapshotCheckpoint
from simulator.mtdnetwork.operation.attack_operation import AttackOperation
from simulator.mtdnetwork.component.host import Host
from simulator.mtdnetwork.component.adversary import Adversary

# from simulator.mtdnetwork.data.constants import ATTACKER_THRESHOLD, OS_TYPES
# from simulator.mtdnetwork.configs import config,set_config
from simulator.mtdnetwork import configs
from simulator.mtdnetwork.operation.mtd_operation import MTDOperation
from simulator.mtdnetwork.component.time_network import TimeNetwork
import matplotlib.pyplot as plt
import warnings
import os
import sys


logger = logging.getLogger()
print("__name__", __name__)
logger.info("init adapter")
# current_directory = os.path.dirname(os.path.abspath(__file__))
# target_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'experiments')
# target_directory = os.getcwd()
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the "s" directory
target_directory = os.path.join(current_script_dir, "..")
print("target_directory", target_directory)
if not os.path.exists(target_directory + "/experimental_data"):
    os.makedirs(target_directory + "/experimental_data")
    os.makedirs(target_directory + "/experimental_data/plots")
    os.makedirs(target_directory + "/experimental_data/results")
sys.path.append(target_directory.replace("experiments", ""))
# print(current_directory)
print(target_directory)
warnings.filterwarnings("ignore")
plt.set_loglevel("WARNING")


class GraphEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Host):
            return obj.toJson()
        return json.JSONEncoder.default(self, obj)


def create_sim(
    start_time=0,
    finish_time=None,
    checkpoints=None,
    new_network=False,
    scheme="random",
    mtd_interval=None,
    custom_strategies=None,
    total_nodes=50,
    total_endpoints=5,
    total_subnets=8,
    total_layers=4,
    target_layer=4,
    total_database=2,
    terminate_compromise_ratio=0.8,
    callback=None,
):
    """The `create_sim` function creates a simulation environment for a network attack and defense
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

    """
    logger.info("init simulation")
    env: simpy.Environment = simpy.Environment()
    snapshot_list: list = []
    end_event = env.event()
    snapshot_checkpoint = SnapshotCheckpoint(env=env, checkpoints=checkpoints)
    time_network = None
    adversary = None

    if start_time > 0:
        try:
            time_network, adversary = snapshot_checkpoint.load_snapshots_by_time(
                start_time
            )
        except FileNotFoundError:
            print("No timestamp-based snapshots available! Set start_time = 0 !")
            return
    elif not new_network:
        try:
            (
                time_network,
                adversary,
            ) = snapshot_checkpoint.load_snapshots_by_network_size(total_nodes)
        except FileNotFoundError:
            print("set new_network=True")
    else:
        time_network = TimeNetwork(
            total_nodes=total_nodes,
            total_endpoints=total_endpoints,
            total_subnets=total_subnets,
            total_layers=total_layers,
            target_layer=target_layer,
            total_database=total_database,
            terminate_compromise_ratio=terminate_compromise_ratio,
        )
        adversary = Adversary(
            network=time_network,
            attack_threshold=configs.config.get("ATTACKER_THRESHOLD"),
        )
        # snapshot_checkpoint.save_to_array(time_network, adversary, res)

    # start attack
    attack_operation = AttackOperation(
        env=env,
        end_event=end_event,
        callback=callback,
        adversary=adversary,
        proceed_time=0,
    )
    attack_operation.proceed_attack()

    # start mtd
    if scheme != "None":
        mtd_operation = MTDOperation(
            env=env,
            end_event=end_event,
            network=time_network,
            scheme=scheme,
            attack_operation=attack_operation,
            proceed_time=0,
            mtd_trigger_interval=mtd_interval,
            custom_strategies=custom_strategies,
        )
        mtd_operation.proceed_mtd()

    # save snapshot by time
    # print("proceed save checkpoints",checkpoints)
    if checkpoints is not None:
        snapshot_checkpoint.proceed_save(time_network, adversary, snapshot_list)

    # Evaluate the simulation
    # evaluation = Evaluation(network=time_network, adversary=adversary)
    
    # start simulation
    if finish_time is not None:
        env.run(until=(finish_time - start_time))
    else:
        env.run(until=end_event)

    evaluation = Evaluation(network=time_network, adversary=adversary)
    # evaluation.save_all()
    # print("RES:",res)
    print("get_compromised_hosts ", evaluation._adversary.get_compromised_hosts())
    return {"evaluation": evaluation, "snapshots": snapshot_list}
