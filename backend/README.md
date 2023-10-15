
# Running the application 

## Using Docker
This web-application has been configured to use a docker container, so can be launched 
simply using that. Ensure you are working from the main directory, then use the following 
command to activate the web-app using docker: 

>  `docker-compose up -d --build`

The application should then launch on localhost:8080.

## Building without docker
If you cannot install docker, then the steps below can be tried. Although the functionality should be similar the application 
is intended to be built through docker, so these steps are not guaranteed to have the exact same results. 

Ensure you have python3 installed. This project was tested using python3.9. Install venv, a python module for creating virtual environments. 

>`python3 -m pip install --user virtualenv`

Create the virtual environment:

>`python3 -m venv mtdgui_env`

Activate the virtual environment:

>`source mtdgui_env/bin/activate`

If done correctly, `(mtdgui_env)` should appear to the left of the terminal. Then, install the dependencies: 

>`pip install -r requirements.txt`
 
### Running the backend 

Open a terminal running your conda environment in the base project directory \\CITS3200. Run the following commands to start the API. 

> `cd backend/mtdgui`

> `uvicorn main:app`

# Running tests 

Open a terminal running your conda environment in the base project directory \\CITS3200. Run the following commands to execute the tests. 

> `cd mtdgui`

> `python -m pytest -rx -W ignore::DeprecationWarning`

# System design 

As mentioned in the main README, our application builds off the MTDSimTime repository, so for simulation errors or implementation details focus on the backend/mtdgui/simulator repository. This section will briefly describe how the simulator works, and how we have integrated it into out application.  

## Simulation operation

The simulation relies on two main sets of parameters - the individual parameters required to set up an instance of the simulation, and the overall configurations used by the simulation throughout its execution. These have been seperated in our application into the paramaters panel (for instance set ups) and the advanced options (for overall configurations). 

The setup variables are passed to adapter class we made to integrate the simulation with our web app. This file can be found at /backend/mtdgui/simulator/adapter.py. This defines the create_sim function that is used to initialise a simulation environment. When the simulation is run, the simpyEnv event is used to track the time taken and which events have occurred. In order to capture the simulation state so it can displayed on the frontend, we have used the NetworkSnapshot.savenetworkarray function. This saves the states at every interval given by the checkpoints value of the submitted parameters, and stores it in an array. This array is returned on the completion of the function and contains the relevant states.

The optional configuration variables have been refactored from the original MTDSimTime repository, and now uses a json configuration file. The optional configuration variables are merged with the default configuration variables to create the configuration variables the simulation will use. Then, this configuration is set and the simulation runs using this new configuration. 