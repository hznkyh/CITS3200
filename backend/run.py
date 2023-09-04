import sys
import os
from pathlib import Path
import threading

# Get the absolute path of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the "s" directory
s_directory = os.path.join(current_script_dir, "..", "simulator")

# Add the "s" directory to the Python path
sys.path.append(s_directory)
from adapter import *
# a= sim_params()
# print(a)
# checks()

import simpy
env = simpy.Environment()
simulation_thread = None
# evaluation , res = run_sim(env, start_time=0, finish_time= 4)
evaluation , res = create_sim(env, start_time=0, finish_time= 4)
simulation_thread = threading.Thread(target=env.run, args=(([2])))
simulation_thread.start()
simulation_thread.join()
print(simulation_thread.is_alive())

print(res, evaluation.get_network().graph.number_of_nodes(), sep='\n')