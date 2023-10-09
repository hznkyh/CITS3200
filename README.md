# About 

This is a web based application designed to help users learn about Moving Target Defence (MTD) techniques. 
After launching the application using the instructions below, the simulator page can be used to visualise 
MTD techniques with various configurations. Up to 5 graphs can be displayed at any given time, and the results 
can be compared graphically with the statistics below each graph. 

# Detailed usage 

## Running the application 

### Using Docker

This web-application has been configured to use a docker container, so can be launched 
simply using that. If you do not have docker, download it from [here](https://www.docker.com/products/docker-desktop/). 
Ensure you are working from the main directory, then use the following 
command to activate the web-app using docker: 

>  `docker-compose up -d --build`

The application should then launch on localhost:8080

## Navigating to the simulation

Open the application on localhost:8080, and use the navigation bar to click the 'Simulation' tab.

## Producing simulated networks 

The simulation should have an instructions tab at the top detailing how the simulation operates. The parameters panel specifies what configuration variables you want to simulate. 
1. After inputting some parameters, you have to save them using the 'Save' button. 
    * Click on the Advanced tab for more configuration options. 

2. After creating the desired number of graphs using the 'Add Graph' button and saving their individual configurations, press the 'Submit' button to generate the graphs. 

3. If the above steps have been performed correctly, you should see a message saying 'Receiving graph...'. The generation of the graphs may take some time so please be patient. 

4. After all graphs have been completed, you should see a message saying 'Got graph'. You are now free to examine the results of the graphs. 

## Evaluating the simulation results

Now the simulations should be complete, and a timeline of the simulation and final results can be observed. 

1. Scroll down until you see a box 'Simulation X', where X is the graph you want to examine. 

2. Click that box. A graph container should appear. 

3. Click 'Start' to automatically walk through all snapshots, or 'Step' to just view the next snapshot. Compromised nodes appear red, and uninfected nodes appear green. 

4. To view aggregated results for the simulation, click one of the four buttons at the bottom of the container. These should display statistic graphs obtained at the end of the simulation. 


## Simulation details

This application has been built off of the MTDSimTime and other repositories here. For more 
detailed information about MTD techniques, please check out the following links.

[MTDSimTime](https://github.com/MoeBuTa/MTDSimTime): The simulation used for our application. 

# Scope for future work

## Expanding advanced configuration options 

The advanced configuration is set using backend/mtdgui/simulator/mtdnetwork/configs.py. 
This will read by default from a default_config.json file (mtdnetwork/data/default_config.json) containing the default 
configuration variables. A full list of variables that can be added to the configuration 
options can be found in that file. 

Currently, when advanced parameters are submitted by the user they are handled by the multi-graph-params endpoint, and are processed in the 
backend/mtdgui/controllers/pools.py handleRequest() function. The current processing should work when adding more options. To add more options, some changes to the frontend and backend will be necessary.  

### Backend requirements 

The models will have to be updated to receive the updated configurations. In models/forms.py create a new Class inheriting BaseModel, and add the required variables. The attributes should have exactly the same names as the keys and values in the default_config.json file, as they are simply merged with the defaults to create the final config used in the simulations. 

After creating the model, add it to the ConfigModel class. As they are optional use Union\[Class_Name,None] so that None is used by default, as None values from input parameters are ignored when creating the final configuration. 


### Frontend requirements 

## Storing previous simulations 