<template>
  <div class="content">
    <button class="instructions" @click="toggleInstructions">{{ showInstructions ? 'Hide Instructions' : "Show Instructions" }}</button>
    <div class="instruction-box" v-if="showInstructions">
      <h1 class="h1-instructions"> Panel Instructions</h1>
      <ol class="list">
        <li>Enter you desired values into the fields below.</li>
        <li>Optional: Click on "Advanced", and enter the inputs for the advanced options. Otherwise, leave it empty (this will set them to the default values).</li>
        <li>Once all fields have been entered, click the save button.</li>
        <li>Optional: If you desire more than one simulation, repeat the previous steps (this will max out at 5).</li>
        <li>Once you have saved your simulation(s), click on submit to submit your data.</li>
        <li>Note: If an error occurs, refer the the popup box on the right side of the page.</li>
      </ol>
      <h3><span style="color: red;">IMPORTANT</span></h3>
      <ol>
        <li>Please fill out a parameter form for each of the simulations if you add more than one, otherwise you will get an error.</li>
        <li>Please be patient when the simulation(s) is/are loading.</li>
      </ol>
      <h1 class="h1-instructions">Simulation Instructions</h1>
      <ol class="list">
        <li>Click on <i class="bi bi-play"></i> to start the simulation</li>
        <li>Click on <i class="bi bi-pause"></i> to stop the simulation</li>
        <li>Click on <i class="bi bi-skip-forward"></i> to step through the simulation</li>
        <li>Click on <i class="bi bi-skip-backward"></i> to step back through the simulation</li>
      </ol>
      <h1 class="h1-instructions">To view</h1>
      <p class="p-instructions">To adjust the view port of the network, click on the buttons "Fit", "Zoom In" and "Zoom Out".</p>
      <p class="p-instructions">Click on an empty space to drag the whole network graph. Place the cursor inside the box, and scroll up and down to zoom in and out respectively.</p>
      <p class="p-instructions">Click a node and hold it to drag it to anyplace desriable.</p>
      <h3>Graph</h3>
      <p class="p-instructions">The graph will show the network and the nodes. The nodes will be coloured based on their state. The legend is as follows:</p>
      <ul class="list">
        <li>Green: Not compromised and exposed<span class="dot" style="background-color: green;"></span></li>
        <li>Yellow: Exposed<span class="dot" style="background-color: yellow;"></span></li>
        <li>Red: Compromised<span class="dot" style="background-color: red;"></span></li>
      </ul>
      <h3>Node</h3>
      <p class="p-instructions">Clicking on a node will show the node's information. The information is as follows:</p>
      <ul class="list">
        <li>OS Type</li>
        <li>OS Version</li>
        <li>Host IP</li>
        <li>HosT ID</li>
        <li>P U Compromise</li>
        <li>Total users</li>
        <li>UUID</li>
        <li>Total services</li>
        <li>Total Nodes</li>
        <li>Compromised</li>
        <li>Compromised Services</li>
      </ul>
    </div>
    <div id="notification-container"></div>
    <div class="panel">
      <form id="paramForm" v-on:submit.prevent="saveForm" >
        <!-- Row 1 -->
        <div class="row">
          <h2> Parameters Panel</h2>

          <div class="group">
            <label>Simulation Number <span style="color: red;">*</span>: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">What simulation you would like to set configurations for.</span>
              </span>
            </div>
            <select id="param" type="text" placeholder="Simulation Number" v-model="graphNum" name="Graph Number" required>
            </select>
          </div>

          <div class="group">
            <label>Number of Nodes <span style="color: red;">*</span>:</label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">The number of nodes in the network (network size). This value needs to be greater than or equal to 20. E.g., 100</span>
              </span>
            </div>
            <input id="param" type="text" placeholder="Number of Nodes..." v-model="nodeNumber" name="total_nodes" required>
          </div>
        

          <div class="group">
            <label>Number of Exposed Nodes <span style="color: red;">*</span>: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">The number of exposed nodes in the network. E.g., 5</span>
              </span>
            </div>
            <input id="param" type="text" placeholder="Number of Exposed Nodes..." v-model="nodeExposed" name="total_endpoints" required>
          </div>
        </div>

          <!-- Row 2 -->
        <div class="row">
          <div class="group">
            <label>Number of Layers <span style="color: red;">*</span>: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">The number of layers in the network. Must be less than or equal to 6. E.g., 4</span>
              </span>
            </div>
            <input id="param" type="text" placeholder="Number of Layers..." v-model="layers" name="total_layers" required>
          </div>
        
          <div class="group">
            <label>Compromise Ratio <span style="color: red;">*</span>: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">The ratio number that will terminate the simulation if reached. This value need to be greater than 0 and less than 1. E.g., 0.8</span>
              </span>
            </div>
            <input id="param" type="text" placeholder="Compromise Ratio..." v-model="compromisedRatio" name="terminate_compromise_ratio" required>
          </div>

          <div class="group">
            <label>MTD Interval <span style="color: red;">*</span>: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">The time interval to trigger an MTD(s). E.g., 5</span>
              </span>
            </div>
            <input id="param" type="text" placeholder="MTD Interval..." v-model="interval" name="mtd_interval" required>
          </div>
        </div>

          <!-- Row 3 -->
        <div class="row">
          <div class="group">
            <label>Finish Time <span style="color: red;">*</span>: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">How long the simulation should run for. This value needs to be greater than 3000.</span>
              </span>
            </div>
            <input id="param" type="text" placeholder="Finish Time..." v-model="finishTime" name="finish_time" required>
          </div>
        

        
          <div class="group">
            <label>Checkpoints <span style="color: red;">*</span>: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">How often snapshots are taken of the simulation. This value needs to be greater than 1000.</span>
              </span>
            </div>
            <input id="param" type="text" placeholder="Checkpoints..." v-model="checkpoints" name="checkpoints" required>
          </div>

          <div class="group">
            <label>Scheme <span style="color: red;">*</span>: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">How the simulator will run. Choose from: random (default), simultaneous, alternative, single and none.</span>
              </span>
            </div>
            <select id="param" type="text" placeholder="Scheme..." v-model="scheme" name="scheme" required>
              <option value="random">random</option>
              <option value="simultaneous"> simultaneous</option>
              <option value="alternative">alternative</option>
              <option value="single">single</option>
              <option value="None">none</option>
            </select>
          </div>
        </div>

        <p id="advanced" class="advanced" @click="toggleAdvanced()">Advanced</p>
        <div id="advancedPanel" class="hidden">
          <div class="row">
            <div class="group">
              <label>Total Subnets: </label>
              <div class="tooltip-container">
                <span id="tooltip">
                  <span class='info'>
                    <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                  </span>
                  <span class="tip">The number of subnets. E.g., 4</span>
                </span>
              </div>
              <input id="param" type="text" placeholder="Total Subnets..." v-model="totalSubnets" name="total_subnets">
            </div>

            <div class="group">
              <label>Target Layer: </label>
              <div class="tooltip-container">
                <span id="tooltip">
                  <span class='info'>
                    <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                  </span>
                  <span class="tip">Target a specfic layer. Must be within the range of input of total layers. E.g., 4</span>
                </span>
              </div>
              <input id="param" type="text" placeholder="Target Layers..." v-model="targetLayers" name="target_layers">
            </div>
          </div>

          <div >
            <span id="tooltip">
              <label id="heading">MTD Priority</label>
              <div class="tooltip-container">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">Below you have the choice to change the priority of options the defender has to avoid an attack. By default (leave empty) it is ordered 1 to 7 from top to bottom. If you wish
                  to change the order please fill in the form.
                </span>
            </div>
            </span>
          </div>

          <div class="row">
            <div class="group">
              <label>Complete Topology Shuffle: </label>
              <input id="param" type="text" placeholder="Complete Topology Shuffle..." name="CompleteTopologyShuffle" v-model="compTopoShuffle">
            </div>
            <div class="group">
              <label>Host Topology Shuffle: </label>
              <input id="param" type="text" placeholder="Host Topology Shuffle..." name="HostTopologyShuffle" v-model="hostTopoShuffle">
            </div>
            <div class="group">
              <label>IP Shuffle: </label>
              <input id="param" type="text" placeholder="IP Shuffle..." name="IPShuffle" v-model="ipShuffle">
            </div>
          </div>

          <div class="row">
            <div class="group">
              <label>OS Diversity: </label>
              <input id="param" type="text" placeholder="OS Diversity..." name="OSDiversity" v-model="osDiveristy">
            </div>
            <div class="group">
              <label>Port Shuffle: </label>
              <input id="param" type="text" placeholder="Port Shuffle..." name="PortShuffle" v-model="portShuffle">
            </div>
            <div class="group">
              <label>Service Diversity: </label>
              <input id="param" type="text" placeholder="Service Diversity..." name="ServiceDivesity" v-model="ServDiversity">
            </div>
            <div class="group">
              <label>User Shuffle: </label>
              <input id="param" type="text" placeholder="User Shuffle..." name="UserShuffle" v-model="userShuffle">
            </div>
          </div>

          <div>
            <span id="tooltip">
              <label id="heading">MTD Trigger Interval</label>
              <div class="tooltip-container">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">When to trigger the chosen scheme
                </span>
              </div>
            </span>
          </div>

          <div class="row">
            <div class="group">
              <label>Simultaneous: </label>
              <input id="param" type="text" placeholder="value,value" name="simultaneous" v-model="similtaneous">
            </div>
            <div class="group">
              <label>Random: </label>
              <input id="param" type="text" placeholder="value,value" name="random" v-model="random">
            </div>
            <div class="group">
              <label>Alternative: </label>
              <input id="param" type="text" placeholder="value,value" name="alternative" v-model="alternative">
            </div>
          </div>
        </div>

        <div class="row">
          <div class="group">
            <button class="saveButton">Save Current Simulation</button>
          </div>
          <div class="group">
            <input type="submit" value="Submit All Simulations" @click="submitForm">
          </div>
        </div>
        
        
        </form>
        <p class="message"> {{ msg }} </p>
    </div>
    <div class="network">
      <Graph @addGraph="handleAddGraph" @removeGraph="handleRemoveGraph" :key="componentKey"></Graph>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Graph from './Graph.vue';

export default {
  name: 'MTDSimulator',
  components: {
    Graph,
  },
  data(){
    return{
      msg: '',
      graphNum: '',
      nodeNumber:'',
      nodeExposed:'',
      layers:'',
      compromisedRatio:'',
      scheme:'',
      interval:'',
      finishTime: '',
      checkpoints: '',
      totalSubnets: '',
      targetLayers: '',
      compTopoShuffle:'',
      hostTopoShuffle:'',
      ipShuffle:'',
      osDiveristy:'',
      portShuffle:'',
      ServDiversity:'',
      userShuffle:'',
      similtaneous:'',
      random:'',
      alternative:'',
      showInstructions: false,
      schemeGraph:'random',
      savedForms: {},
      componentKey: 0,
    };
  },

  methods: {
    forceRerender() {
      this.componentKey += 1;
    },
    handleAddGraph(name){
      //console.log(name)
      const paramSelect = document.getElementById('param');

      if (paramSelect.options.length >=5){
        this.showNotification("You can only add up to 5 graphs.");
        return;
      }
      const newOption = document.createElement('option');
      newOption.text = name;
      newOption.value = name;
      newOption.id = name

      paramSelect.appendChild(newOption);
    },

    handleRemoveGraph(name) {
      const option = document.getElementById(name);
      //console.log("Picked " + option);
      option.remove()
      axios.post(`/network/remove/${name}`);
      delete this.savedForms[name];
    },

    test() {
      Graph.methods.revealLabel(2);
    },
    toggleAdvanced(){
      var advancedContent = document.getElementById("advancedPanel");
      if (advancedContent.classList.contains("hidden")) {
        advancedContent.classList.remove("hidden");
      }  else {
        advancedContent.classList.add("hidden");
      }
    },
    saveForm(){
      if(Object.keys(this.savedForms).length <= 5){
        const validationRules = [
          {field: this.nodeNumber, validator: this.validateNodes, fieldName: 'Number of Nodes'},
          {field: this.nodeExposed, validator: this.validateIntInputs, fieldName: 'Nodes Exposed'},
          {field: this.layers, validator: this.validateLayers, fieldName: 'Number of Layers'},
          {field: this.compromisedRatio, validator: this.validateRatio, fieldName: 'Compromise Ratio'},
          {field: this.scheme, validator: this.validateWord, fieldName: 'Scheme'},
          {field: this.interval, validator: this.validateFloatInputs, fieldName: 'MTD Interval'},
          {field: this.finishTime, validator: this.validateFinishTime, fieldName: 'Finish Time'},
          {field: this.checkpoints, validator: this.validateCheckpoints, fieldName: 'Checkpoints'},
          {field: this.totalSubnets, validator: this.validateTotalSubnets, fieldName: 'Total Subsets'},
          {field: this.targetLayers, validator: this.validateTargetLayer, fieldName: 'Target Layers'},
          {field: this.compTopoShuffle, validator: this.validatePrioityInput, fieldName: 'Complete Topology Shuffle'},
          {field: this.hostTopoShuffle, validator: this.validatePrioityInput, fieldName: 'Host Topology Shuffle'},
          {field: this.ipShuffle, validator: this.validatePrioityInput, fieldName: 'IP Shuffle'},
          {field: this.osDiveristy, validator: this.validatePrioityInput, fieldName: 'OS Diversity'},
          {field: this.portShuffle, validator: this.validatePrioityInput, fieldName: 'Port Shuffle'},
          {field: this.ServDiversity, validator: this.validatePrioityInput, fieldName: 'Service Diversity'},
          {field: this.userShuffle, validator: this.validatePrioityInput, fieldName: 'User Shuffle'},
          {field: this.similtaneous, validator: this.validateTrigger, fieldName: 'Simultaneous'},
          {field: this.random, validator: this.validateTrigger, fieldName: 'Random'},
          {field: this.alternative, validator: this.validateTrigger, fieldName: 'Alternative'}
      ];

      const errorMessages = [];

      validationRules.forEach(rule => {
        if (!rule.validator(rule.field)) {
          errorMessages.push(`Invalid input for ${rule.fieldName}`);
        }
      });
      console.log(errorMessages);
      if (errorMessages.length === 0) {
        ////console.log('Correct inputs have been detected');
        var mainData = {
          "graph": {
            "graph_name": this.graphNum,
          },
          "run": {
            "total_nodes": this.nodeNumber,
            "total_endpoints": this.nodeExposed,
            "total_layers": this.layers,
            "terminate_compromise_ratio": this.compromisedRatio,
            "scheme": this.scheme,
            "mtd_interval": this.interval,
            "finish_time": this.finishTime,
            "checkpoints": this.checkpoints,
            "total_subnets": this.totalSubnets !== '' ? parseInt(this.totalSubnets) : null,
            "target_layer": this.targetLayers !== '' ? parseInt(this.targetLayers) : null,
          },
          "config": this.checkAdvancedDataEntered(errorMessages)
        };
        if (errorMessages.length === 0) {
          this.msg = 'Saved parameters for ' + this.graphNum;
          // var data = JSON.stringify(mainData);
          // this.savedForms.push(mainData);
          var cur_graph = this.graphNum;
          //console.log("NAME" ,cur_graph)
          this.savedForms[cur_graph] = mainData; 
          console.log(this.savedForms);
        }
      }

      else{
        this.showNotification(`Validation Errors:`,errorMessages);
      }
      }
      else{
        this.showNotification('Can only save up to five Graphs at a time',errorMessages);
      }
    },

    resetForm(){
      this.savedForms = {};

      this.graphNum = ''
      this.nodeNumber = ''
      this.nodeExposed = ''
      this.layers = ''
      this.compromisedRatio = ''
      this.scheme = ''
      this.interval = ''
      this.finishTime = ''
      this.checkpoints = ''
      this.totalSubnets = ''
      this.targetLayers = ''
      this.compTopoShuffle = ''
      this.hostTopoShuffle = ''
      this.ipShuffle = ''
      this.osDiveristy = ''
      this.portShuffle = ''
      this.ServDiversity = ''
      this.userShuffle = ''
      this.similtaneous = ''
      this.random = ''
      this.alternative = ''
    },
  
    submitForm() {
      this.msg = 'Saved parameters';

      ////console.log(this.savedForms);

      // const formData = JSON.parse(savedForm);
      var cur_sims = document.querySelectorAll(".sim-label");
      //console.log(document.querySelectorAll(".sim-label"));
      //console.log(this.savedForms);
      var matches = 0;
      var num_forms = Object.keys(this.savedForms).length; 
      var keys = Object.keys(this.savedForms);
      if (num_forms == cur_sims.length){ 
        for (let i = 0; i<cur_sims.length;i++){ 
          var selected_name = cur_sims[i].textContent; 
          //console.log("element exists at " + selected_name);
          if (selected_name in this.savedForms){ 
            //console.log("Matched " + selected_name);
            matches++; 
          } 
        }
      }
      if (matches != cur_sims.length || cur_sims.length == 0){ 
        //THROW ERROR 
        this.showNotification("Names do not match, resetting forms.");
        // print error message - tell resetting forms 
        // //console.log("matched a total of " + matches)
        // //console.log("THROWING ERROR :(())")
        this.resetForm();
        return ; 
      }

      //console.log("SAVED " , JSON.stringify(this.savedForms));
      axios
        .post('/network/multi-graph-params', JSON.stringify(this.savedForms), {
          headers: { 'Content-Type': 'application/json' },
        })
        .then(async (response) => {
          ////console.log(response);
          this.msg = 'Receiving graph(s)...';

          await Graph.methods.getGraph();
          // this.forceRerender();`
          this.msg = 'Successfully received graph(s)';
        })
        .catch((error) => {
          ////console.error(error);
        });
    },

    validateIntInputs(value){
      if (value === '') {
        return true;
      }
      const parsedValue = parseInt(value);
      return !isNaN(parsedValue) && parsedValue >= 0;
    },
    validateNodes(num){
      const parsedValue = parseInt(num);
      return !isNaN(parsedValue) && parsedValue >= 20;
    },
    validateFloatInputs(value){
      const parsedValue = parseFloat(value);
      return !isNaN(parsedValue) && parsedValue >= 0.0;
    },
    validateLayers(value){
      if (value === '') {
        return true;
      }
      const parsedValue = parseInt(value);
      return !isNaN(parsedValue) && parsedValue >= 0 && parsedValue <= 6;
    },
    validateCheckpoints(value){
      const parsedValue = parseFloat(value);
      return !isNaN(parsedValue) && parsedValue >= 10;
    },
    validateRatio(value){
      const parsedValue = parseFloat(value)
      return !isNaN(parsedValue) && parsedValue >= 0.0 && parsedValue <= 1.0;
    },
    validatePrioityInput(num){
      const parsedValue = parseFloat(num);
      return !isNaN(parsedValue) && parsedValue >= 0 && parsedValue <= 7 || num == '';
    },
    validateWord(word){
      const possibleWords = ['random', 'simultaneous', 'alternative', 'single', 'None'];
        return possibleWords.includes(word);
    },
    validateFinishTime(time){
      const parsedValue = parseFloat(time);
      return !isNaN(parsedValue) && parsedValue >= 3000;
    },
    validateTotalSubnets(num){
      if (num === ''){
        return true;
      }
      const parsedNum = parseFloat(num);
      ////console.log((this.nodeNumber - this.nodeExposed) / (parsedNum - 1))
      if (!isNaN(parsedNum) && (this.nodeNumber - this.nodeExposed) / (parsedNum - 1) > 2) {
        return true;
      }
      return false;
    },
    validateTargetLayer(num){
      if (num === '') {
        return true;
      }
      const parsedValue = parseInt(num);
      return !isNaN(parsedValue) && parsedValue >= 0 && parsedValue <= this.layers;
    },
    validateTrigger(values) {
      if(!values){
        return true;
      }
      const intPattern = /^\d+$/;
      const floatPattern = /^\d+(\.\d+)?$/;
      ////console.log(values)

      const separate = values.split(',').map(part => part.trim());
      ////console.log(separate)
      if (separate.length != 2){
        return false;
      }

      const valueOne = intPattern.test(separate[0]);
      const valueTwo = floatPattern.test(separate[1])

      return valueOne && valueTwo
    },
    checkAdvancedDataEntered(errorMessages) {
      var json_string = new Object();
      var added = 0;
      var uniqueValues = new Set();

      var mtdPriorityInputs = [
        this.compTopoShuffle,
        this.hostTopoShuffle,
        this.ipShuffle,
        this.osDiveristy,
        this.portShuffle,
        this.ServDiversity,
        this.userShuffle
      ]

      for(var i = 0; i < mtdPriorityInputs.length; i++){
        var inputValues = mtdPriorityInputs[i];
        if(inputValues != '');
        var numericValues = parseInt(inputValues);
        if(!isNaN(numericValues)){
          if(numericValues >= 1 && numericValues <=7){
            if (uniqueValues.has(numericValues)){
              errorMessages.push("Host Topology: Duplicate values");
              this.showNotification("Host Topology: Duplicate values");
              return null;
          }
          uniqueValues.add(numericValues);
        } else {
          errorMessages.push("Input values must be between 1 and 7");
          this.showNotification("Input values must be between 1 and 7");
          return null;
          }
        }
      }

      if (
        (this.compTopoShuffle !== '' ||
          this.hostTopoShuffle !== '' ||
          this.ipShuffle !== '' ||
          this.osDiveristy !== '' ||
          this.portShuffle !== '' ||
          this.ServDiversity !== '' ||
          this.userShuffle !== '') &&
        (this.compTopoShuffle === '' ||
          this.hostTopoShuffle === '' ||
          this.ipShuffle === '' ||
          this.osDiveristy === '' ||
          this.portShuffle === '' ||
          this.ServDiversity === '' ||
          this.userShuffle === '')
      ) {
        errorMessages.push("Please fill all the required form boxes in MTD_PRIORITY.");
        this.showNotification("Please fill all the required form boxes in MTD_PRIORITY.");

      } else if (
        this.compTopoShuffle !== '' ||
        this.hostTopoShuffle !== '' ||
        this.ipShuffle !== '' ||
        this.osDiveristy !== '' ||
        this.portShuffle !== '' ||
        this.ServDiversity !== '' ||
        this.userShuffle !== ''
      ) {
        json_string.MTD_PRIORITY = {
          "CompleteTopologyShuffle": this.compTopoShuffle !== '' ? parseInt(this.compTopoShuffle) : null,
          "HostTopologyShuffle": this.hostTopoShuffle !== '' ? parseInt(this.hostTopoShuffle) : null,
          "IPShuffle": this.ipShuffle !== '' ? parseInt(this.ipShuffle) : null,
          "OSDiversity": this.osDiveristy !== '' ? parseInt(this.osDiveristy) : null,
          "PortShuffle": this.portShuffle !== '' ? parseInt(this.portShuffle) : null,
          "ServiceDiversity": this.ServDiversity !== '' ? parseInt(this.ServDiversity) : null,
          "UserShuffle": this.userShuffle !== '' ? parseInt(this.userShuffle) : null,
        };
        added++;
      } else { 
        json_string.MTD_PRIORITY = null
      }

      if (
        (this.similtaneous !== '' ||
          this.random !== '' ||
          this.alternative !== '') &&
        (this.similtaneous === '' ||
          this.random === '' ||
          this.alternative === '')
      ) {
        errorMessages.push("Please fill all the required form boxes in MTD TRIGGER INTERVAL.");
        this.showNotification("Please fill all the required form boxes in MTD TRIGGER INTERVAL.");
        json_string.MTD_TRIGGER_INTERVAL = null;
        
      } else if (
        this.similtaneous !== '' ||
        this.random !== '' ||
        this.alternative !== ''
      ) {
        json_string.MTD_TRIGGER_INTERVAL = {
          "simultaneous": this.similtaneous !== '' ? this.triggerConversion(this.similtaneous) : null,
          "random": this.random !== '' ? this.triggerConversion(this.random) : null,
          "alternative": this.alternative !== '' ? this.triggerConversion(this.alternative) : null,
        };
        added++;
      } else { 
        json_string.MTD_TRIGGER_INTERVAL = null
      }

      ////console.log(json_string);
      return added > 0 ? json_string : null;
    },
    triggerConversion(floatStr){
      const floatArray = floatStr.split(',').map(value => parseFloat(value.trim()));
      return floatArray
    },
    toggleInstructions(){
      this.showInstructions = !this.showInstructions;
    },
    showNotification(title, errorMessages = []) {
      const notification = document.createElement('div');
      notification.className = 'notification';
      if (errorMessages.length == 0) {
        errorMessages.push(title);
      }
      console.log(errorMessages); 
      let errorMessageHTML = "";
      if (errorMessages.length > 0) {
          errorMessageHTML = "<ul>";
          for (const errorMsg of errorMessages) {
              errorMessageHTML += `<li>${errorMsg}</li>`;
          }
          errorMessageHTML += "</ul>";
      }

      notification.innerHTML = `<strong>Validation Error</strong>${errorMessageHTML}`;
      const container = document.getElementById('notification-container');
      container.appendChild(notification);

      setTimeout(() => {
        notification.classList.add('fadeOut');
        setTimeout(() => {
          container.removeChild(notification);
        }, 500);
      }, 5000);
    },
  },
};
</script>

<style>
body, html {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
}
.h1-instructions, .p-instructions {
  text-align: left;
}

.content {
    width: 100%;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 20px;
}

.panel{
    width: 100%;
    max-width: 100%;
    margin-bottom: 20px; 
    background: #ffffff;
    padding: 2em;
    border-radius: 10px;
    margin:2em;
    overflow-y: scroll;
    border: none;
    position: relative;
    box-shadow: 
      inset -2px -2px 5px rgba(255, 255, 255, 0.9), 
      inset 2px 2px 5px rgba(0, 0, 0, 0.2),
      -2px -2px 5px rgba(255, 255, 255, 0.9), 
      2px 2px 5px rgba(0, 0, 0, 0.2);
}

.panel::-webkit-scrollbar {
  width:8px;
  position: absolute;
  right: 10px;
  top: 10px;
  bottom: 10px;
}

.panel::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 4px;
}

.panel::-webkit-scrollbar-thumb:hover{
  background-color: #aaa;
}

.advanced {
  background-color: #ffffff;
  display: inline-block;
  padding: 0.5em 1em;
  width: 100%;
  text-align: center;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px; 
  cursor: pointer;
  transition: all 0.3s ease-in-out; 
  font-weight: 500; 
}

.advanced:hover {
  background-color: #3454a4;
  color: #ffffff;
}

.advanced:active {
  background-color: #2c448c;
}


.hidden{
  display: none;
}

label, input, select {
  width: 100%;
  max-width: 100%;
  margin-bottom: 10px;
}

.network {
  width: 100%;
  margin: 2em;
  margin-top: 20px;
  padding: 2em;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 
  inset -2px -2px 5px rgba(255, 255, 255, 0.9), 
  inset 2px 2px 5px rgba(0, 0, 0, 0.2),
  -2px -2px 5px rgba(255, 255, 255, 0.9), 
  2px 2px 5px rgba(0, 0, 0, 0.2);
}

input[type=text] {
   width: 100%;
   margin: 5px 0 10px 0;
   padding: 10px;
   display: inline-block;
   border: none;
   background: #f5f5ff;
   border-radius: 5px;
   font-size: 16px;
}

input[type=text]:focus {
   background-color: #e0e0e0;
   outline: none;
}
input[type="submit"]{
  background-color: #000;
  color: #fff;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease-in-out;
  margin-bottom: 10px;
  font-weight: 500;
}

input[type="submit"]:hover {
  background-color: #333;
}

input[type="submit"]:active{
  background-color: #222;
}

form {
  padding: 1em;
}

.tooltip-container{
  position: relative;
  display: inline-block;
  vertical-align: auto;
}

.tooltip-container .info{
  cursor: help;
  padding: 0 5px;
  display: inline-block;
}

.tooltip-container .tip {
  position: absolute;
  top: 50%;;
  left: 110%;
  transform: translateY(-50%);
  display: none;
  min-width: 200px;
  padding: 8px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 1;
  font-size: 14px;
  color: #000;
  transition: opacity 0.3s, visibility 0.3s;
}

.tooltip-container .tip::before{
  content: '';
  position: absolute;
  top: -5px;
  left: 50%;
  transform: translatey(-50%);
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-bottom: 6px solid #fff;
  z-index: 0;
}

.tooltip-container:hover .tip{
  display: block;
  opacity: 1;
  visibility: visible;
}
#tooltip{
    text-align: left;
    background-color: transparent;
    border: 0px !important;
    width: auto;
    color: #666666;
    font-size: 14px;
}

#tooltip .info {
  text-decoration: underline;
  font-style: italic;
}

#tooltip .tip { 
     display: none;
}

 #tooltip:hover .tip { 
    display: block;
    color: #333;
    background: #fff;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
 }

 #heading{
  font-size: 20px;
  color: #333;
 }

 .instructions{
    width: 100%;
    background-color: #e2b600;
    color: black;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease-in-out;
    margin-bottom: 15px;
    font-weight: 500;
 }

 .instructions:hover{
  background-color: #D8AC00;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
 }

 .instructions:active{
  background-color: #D8AC00;
 }

 .instruction-box {
    width: 100%;
    margin: 2em;
    margin-top: 20px;
    padding: 2em;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 
      inset -2px -2px 5px rgba(255, 255, 255, 0.9), 
      inset 2px 2px 5px rgba(0, 0, 0, 0.2),
      -2px -2px 5px rgba(255, 255, 255, 0.9), 
      2px 2px 5px rgba(0, 0, 0, 0.2);
 }

 .list {
  margin-bottom: 1em;
 }

.dot {
  height: 0.7em;
  width: 0.7em;
  margin-left: 0.5em;
  border-radius: 50%;
  display: inline-block;
}

.row{
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.group{
  flex: 1;
}

.group .tooltip-container{
  position: relative;
}

.group .info{
  margin-right: 5px;
}

.group select{
  margin-top: 15px;
}

.addGraph{
  width: 100%;
  background-color: #A7C7E7;
  color: black;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease-in-out;
  margin-bottom: 10px;
  font-weight: 500;
 }

 .addGraph:hover{
  background-color: #95B5D7;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
}

.addGraph:active{
  background-color: #95B5D7;
}

.resetButton, .saveButton{
  width: 100%;
  background-color: #000;
  color: #fff;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease-in-out;
  margin-bottom: 10px;
  font-weight: 500;
}

.resetButton:hover, .saveButton:hover{
  background-color: #333;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
}

.resetButton:active, .saveButton:active{
  background-color: #222;
}

#notification-container {
  position: fixed;
  top: 10px;
  right: 10px;
  z-index: 1000;
}

.notification {
  display: inline-block;
  max-width: 80vh;
  background-color: white;
  color: red;
  padding: 10px 20px;
  margin-bottom: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  transition: opacity 0.5s, transform 0.5s;
  white-space: per-line;
}

.notification.fadeOut {
  opacity: 0;
  transform: translateX(100%);
}

.message {
  font-size: 25px;
  font-weight: 500;
}
</style>