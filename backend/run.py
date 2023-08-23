import sys
import os
from pathlib import Path

# Get the absolute path of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the "s" directory
s_directory = os.path.join(current_script_dir, "..", "simulator")

# Add the "s" directory to the Python path
sys.path.append(s_directory)
from adapter import *
test()