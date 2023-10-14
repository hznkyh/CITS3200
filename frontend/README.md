# Frontend
Vite project with node.js and typescript.

## Features
- Customise simulation name
- Send simulation parameter to backend
- Add and remove simulations
- Display received simulation
- Interact with simulations to view metrics
- View aggregated statistics based on simulation
- Simulation control flow

## Design 
Design Decisions
- Vite was used its fast and easy to development platform. It provides a simple HTML template that structures and formats the frontend components, including javascript and CSS in one file. Vite's built-in features such as v-model and v-if, streamline the development process especially for data-binding and conditional rendering.

UI/UX
- The webpage has been designed to be user-friendly. Each component is laid out in a systematic order of how it should be used, with the instructions at the top, followed by the parameter panel and graph addition functionality. The clear layout is both made visually appealing, with clear sections for each component of the page being separated into sections for easy usage.

Architecture
- Using Vue's component system, the frontend has been modularised, making it easier to maintain and extend. Major components has been separated for this reason, these include 'Home.vue', 'MTDSimulator.vue', 'Graph.vue', 'Metrics.vue', and 'NodeInfo.vue'. Where each component is responsible for specfic features of the application.
### Main components 
Home.vue
- Home page of the website
- Descriptions of MTD

MTDSimulator.vue
- Instructions
- Simulation paramter panel

Graph.vue
- Simulation display
- Control flow
- Simulation name customisation

Metrics.vue
- Metrics png display

NodeInfo.vue
- Node information display

## Running the application
Backend should be running before running frontend
### Running docker env 
```
docker build -t frontend
docker run -it frontend 
```

### Running locally
```
see instructions in frontend/Vite/README.md
```


