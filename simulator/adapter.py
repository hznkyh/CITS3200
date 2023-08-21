
import os
import sys
current_directory = os.getcwd()
if not os.path.exists(current_directory + 'experiments/experimental_data'):
    os.makedirs(current_directory + 'experiments/experimental_data')
    os.makedirs(current_directory + 'experiments/experimental_data/plots')
    os.makedirs(current_directory + 'experiments/experimental_data/results')
sys.path.append(current_directory.replace('experiments', ''))
import warnings
import pandas as pd
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.set_loglevel('WARNING')
from experiments.run import single_mtd_simulation, create_experiment_snapshots, execute_simulation
create_experiment_snapshots([25, 50, 75, 100])
test = execute_simulation()
test.visualise_attack_operation()
test.draw_network()
