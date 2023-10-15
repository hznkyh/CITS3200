import logging
import simpy
from simulator.mtdnetwork.statistic.evaluation import Evaluation
from simulator.mtdnetwork.snapshot.snapshot_checkpoint import SnapshotCheckpoint
from simulator.mtdnetwork.operation.attack_operation import AttackOperation
from simulator.mtdnetwork.component.adversary import Adversary
from simulator.mtdnetwork import configs
from simulator.mtdnetwork.operation.mtd_operation import MTDOperation
from simulator.mtdnetwork.component.time_network import TimeNetwork
import matplotlib.pyplot as plt
import warnings
import os
import sys


logger = logging.getLogger()
logger.info("init adapter")
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the "s" directory
target_directory = os.path.join(current_script_dir, "..")

if not os.path.exists(target_directory + "/experimental_data"):
    os.makedirs(target_directory + "/experimental_data")
    os.makedirs(target_directory + "/experimental_data/plots")
    os.makedirs(target_directory + "/experimental_data/results")
sys.path.append(target_directory.replace("experiments", ""))
warnings.filterwarnings("ignore")
plt.set_loglevel("WARNING")

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
    """
    Create a simulation of a network with an adversary and MTD strategies.

    Parameters
    ----------
    start_time : int, optional
        The time at which to start the simulation, by default 0.
    finish_time : int, optional
        The time at which to end the simulation, by default None.
    checkpoints : list, optional
        A list of times at which to save a snapshot of the simulation, by default None.
    new_network : bool, optional
        Whether to create a new network for the simulation, by default False.
    scheme : str, optional
        The MTD scheme to use, by default "random".
    mtd_interval : int, optional
        The interval at which to trigger MTD strategies, by default None.
    custom_strategies : list, optional
        A list of custom MTD strategies to use, by default None.
    total_nodes : int, optional
        The total number of nodes in the network, by default 50.
    total_endpoints : int, optional
        The total number of endpoints in the network, by default 5.
    total_subnets : int, optional
        The total number of subnets in the network, by default 8.
    total_layers : int, optional
        The total number of layers in the network, by default 4.
    target_layer : int, optional
        The target layer for the adversary to attack, by default 4.
    total_database : int, optional
        The total number of databases in the network, by default 2.
    terminate_compromise_ratio : float, optional
        The ratio of compromised nodes at which to terminate the simulation, by default 0.8.
    callback : function, optional
        A function to call at the end of the simulation, by default None.

    Returns
    -------
    dict
        A dictionary containing the evaluation and snapshot data from the simulation.
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
            logger.debug("No timestamp-based snapshots available! Set start_time = 0 !")
            return
    elif not new_network:
        try:
            (
                time_network,
                adversary,
            ) = snapshot_checkpoint.load_snapshots_by_network_size(total_nodes)
        except FileNotFoundError:
            logger.debug("set new_network=True")
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

    return {"evaluation": evaluation, "snapshots": snapshot_list}
