
# Backend setup

This project uses FastAPI for the backend. 

## Setting up the environment

To set up this project, we will use a conda environment. This environment was designed for and tested with a 64 bit Windows environment.

### For Windows 64

Download [miniconda](https://docs.conda.io/projects/miniconda/en/latest/), which will be using to create our virtual environment. 

Install conda, and navigate to the base directory of this repository `\CITS3200`. Run the following commands: 

> `conda create --name mtdgui --file conda-spec.txt`

After creating the conda environment, activate it: 

>`conda activate mtdgui` 

If done correctly, `(mtdgui)` should appear to the left of the terminal. 

### For linux or other OS. 

Warning: This has not been extensively tested. The project dependencies have been provided in the requirements.txt file. Try the steps above, but if they fail the following may work: 

Ensure you have python3 installed. This project was tested using python3.9. Install venv, a python module for creating virtual environments. 

>`python3 -m pip install --user virtualenv`

Create the virtual environment:

>`python3 -m venv mtdgui_env`

Activate the virtual environment:

>`source mtdgui_env/bin/activate`

If done correctly, `(mtdgui_env)` should appear to the left of the terminal. Then, install the dependencies: 

>`pip install -r requirements.txt`
 
## Running the backend 

Open a terminal running your conda environment in the base project directory \\CITS3200. Run the following commands to start the API. 

> `cd backend/mtdgui`

> `uvicorn main:app`

### Running tests 

Open a terminal running your conda environment in the base project directory \\CITS3200. Run the following commands to execute the tests. 

> `cd mtdgui`

> `pytest -rx -W ignore::DeprecationWarning`