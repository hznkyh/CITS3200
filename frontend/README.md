# Frontend
Vite project with node.js and typescript.

## Features
- Customise simulation name
- Send simulation parameter to backend
- Display received simulation
- Simulation control flow

## Design 
### Main components 
Home.vue
- Home page of the website
- Descriptions of MTD

MTDSimulator.vue
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
### Running docker env 
```
docker build -t frontend
docker run -it frontend 
```

### Running locally
```
see instructions in frontend/Vite/README.md
```


