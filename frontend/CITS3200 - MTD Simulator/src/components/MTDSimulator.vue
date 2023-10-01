<template>
  <div class="content">
    <button class="instructions" @click="toggleInstructions">{{ showInstructions ? 'Hide Instructions' : "Show Instructions" }}</button>
    <div class="instruction-box" v-if="showInstructions">
      <h1>Instructions</h1>
      <ol class="list">
        <li>Enter inputs to the panel at the right</li>
        <li>Optional: Click on "Advanced", and enter input for advanced options. Otherwise, leave it as the default values.</li>
        <li>Click on "Start" to start the simulation</li>
        <li>Click on "Step" to step through the simulation</li>
        <li>Click on "Stop" to stop the simulation</li>
      </ol>
      <h1>To view</h1>
      <p>To adjust the view port of the network, click on the buttons "Fit", "Zoom In" and "Zoom Out".</p>
      <p>Click on an empty space to drag the whole network graph. Place the cursor inside the box, and scroll up and down to zoom in and out respectively.</p>
      <p>Click a node and hold it to drag it to anyplace desriable.</p>
      <h3>Graph</h3>
      <p>The graph will show the network and the nodes. The nodes will be coloured based on their state. The legend is as follows:</p>
      <ul class="list">
        <li>Green: Not compromised and exposed<span class="dot" style="background-color: green;"></span></li>
        <li>Yellow: Exposed<span class="dot" style="background-color: yellow;"></span></li>
        <li>Red: Compromised<span class="dot" style="background-color: red;"></span></li>
      </ul>
      <h3>Node</h3>
      <p>Clicking on a node will show the node's information. The information is as follows:</p>
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
    <div class="panel">
      <form id="paramForm" v-on:submit.prevent="submitForm" >
        <!-- Row 1 -->
        <div class="row">
          <h2> Parameters Panel</h2>

          <div class="group">
            <label>Graph Number *: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">What graph you would like to set configurations for.</span>
              </span>
            </div>
            <select id="param" type="text" placeholder="Graph Number" v-model="graphNum" name="Graph Number" required>
              <option value="graph1">Graph 1</option>
            </select>
          </div>

          <div class="group">
            <label>Number of Nodes *:</label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">The number of nodes in the network (network size). E.g., 100</span>
              </span>
            </div>
            <input id="param" type="text" placeholder="Number of Nodes..." v-model="nodeNumber" name="total_nodes" required>
          </div>
        

          <div class="group">
            <label>Number of Exposed Nodes *: </label>
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
            <label>Number of Layers *: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">The number of layers in the network. E.g., 4</span>
              </span>
            </div>
            <input id="param" type="text" placeholder="Number of Layers..." v-model="layers" name="total_layers" required>
          </div>
        
          <div class="group">
            <label>Compromise Ratio *: </label>
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
            <label>MTD Interval *: </label>
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
            <label>Finish Time *: </label>
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
            <label>Checkpoints *: </label>
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
            <label>Scheme *: </label>
            <div class="tooltip-container">
              <span id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">How the simulator will run. Chose from: random (default), simultaneous, alternative, single and none.</span>
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
              <label>Target Layers: </label>
              <div class="tooltip-container">
                <span id="tooltip">
                  <span class='info'>
                    <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                  </span>
                  <span class="tip">How often snapshots are taken of the simulation. E.g., 4</span>
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
              <input id="param" type="text" placeholder="(value, value)" name="simultaneous" v-model="similtaneous">
            </div>
            <div class="group">
              <label>Random: </label>
              <input id="param" type="text" placeholder="(value, value)" name="random" v-model="random">
            </div>
            <div class="group">
              <label>Alternative: </label>
              <input id="param" type="text" placeholder="(value, value)" name="alternative" v-model="alternative">
            </div>
          </div>
        </div>

        <input type="submit" value="Submit">
        </form>
        <p class="message"> {{ msg }} </p>
    </div>
    <span @click="test">Test</span>
    <div class="network">
      <Graph></Graph>
    </div>
    <button class="addGraph" @click="addGraph">Add Graph</button>
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
    };
  },

  methods: {
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
  
    submitForm(){
      const validationRules = [
        {field: this.nodeNumber, validator: this.validateNodes, fieldName: 'Node Number'},
        {field: this.nodeExposed, validator: this.validateIntInputs, fieldName: 'Nodes Exposed'},
        {field: this.layers, validator: this.validateIntInputs, fieldName: 'Number of Layers'},
        {field: this.compromisedRatio, validator: this.validateRatio, fieldName: 'Compromise Ratio'},
        {field: this.scheme, validator: this.validateWord, fieldName: 'Scheme'},
        {field: this.interval, validator: this.validateFloatInputs, fieldName: 'MTD Interval'},
        {field: this.finishTime, validator: this.validateFinishTime, fieldName: 'Finish Time'},
        {field: this.checkpoints, validator: this.validateCheckpoints, fieldName: 'Checkpoints'},
        {field: this.totalSubnets, validator: this.validateTotalSubnets, fieldName: 'Total Subsets'},
        {field: this.targetLayers, validator: this.validateIntInputs, fieldName: 'Target Layers'},
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

      if (errorMessages.length === 0) {
        console.log('Correct inputs have been detected');
         // For config, for each field check if they have been entered and return null if not: 
        // For config overall, return null if no fields have been entered 
          var mainData = ({
            "graph":{
              "graph_number": this.graphNum,
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
            "config": this.checkAdvancedDataEntered()
            // "config": this.ipShuffle !== '' ? { 
            //   MTD_PRIORITY: this.ipShuffle !== '' ?  {
            //     "CompleteTopologyShuffle": this.compTopoShuffle !== '' ? parseInt(this.compTopoShuffle) : null,
            //     "HostTopologyShuffle": this.hostTopoShuffle !== '' ? parseInt(this.hostTopoShuffle) : null,
            //     "IPShuffle": this.ipShuffle !== '' ? parseInt(this.ipShuffle) : null,
            //     "OSDiveristy": this.osDiveristy !== '' ? parseInt(this.osDiveristy) : null,
            //     "PortShuffle": this.portShuffle !== '' ? parseInt(this.portShuffle) : null,
            //     "ServiceDiversity": this.ServDiversity !== '' ? parseInt(this.ServDiversity) : null,
            //     "UserShuffle": this.userShuffle !== '' ? parseInt(this.userShuffle) : null,
            //   } : null,
            //   MTD_TRIGGER_INTERVAL: this.similtaneous !== '' ? {
            //     "simultaneous": this.similtaneous !== '' ? parseInt(this.similtaneous) : null,
            //     "random": this.random !== '' ? parseInt(this.random) : null,
            //     "alternative": this.alternative !== '' ? parseInt(this.alternative) : null,
            //   } : null,
            // }: null,
          });
          this.msg = 'Getting graph';
          var data = JSON.stringify(mainData);
          console.log(data)
          //console.log(data);
          axios.post('/network/update_all_params/', data, {headers: {'Content-Type': 'application/json'}})
          .then(async (response) => {
            console.log(response);
            await Graph.methods.getGraph();
            this.msg = 'Got graph';
          }) .catch((error) => {
            console.log(error);
          });
      }
      else{
        alert(`Validation Errors:\n${errorMessages.join('\n')}`);
      }
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
    validateCheckpoints(value){
      const parsedValue = parseFloat(value);
      return !isNaN(parsedValue) && parsedValue >= 1000;
    },
    validateRatio(value){
      const parsedValue = parseFloat(value)
      return !isNaN(parsedValue) && parsedValue <= 1.0;
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
      console.log((this.nodeNumber - this.nodeExposed) / (parsedNum - 1))
      if (!isNaN(parsedNum) && (this.nodeNumber - this.nodeExposed) / (parsedNum - 1) > 2) {
        return true;
      }
      return false;
    },
    validateTrigger(values) {
      if(!values){
        return true;
      }
      const intPattern = /^\d+$/;
      const floatPattern = /^\d+(\.\d+)?$/;
      console.log(values)

      const separate = values.split(',').map(part => part.trim());
      console.log(separate)
      if (separate.length != 2){
        return false;
      }

      const valueOne = intPattern.test(separate[0]);
      const valueTwo = floatPattern.test(separate[1])

      return valueOne && valueTwo
    },
    checkAdvancedDataEntered() {
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
              alert("Values 1 to 7 can only input once.");
              return null;
          }
          uniqueValues.add(numericValues);
        } else {
          alert("Input values must be between 1 and 7");
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
        alert("Please fill all the required form boxes in MTD_PRIORITY.");

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
        alert("Please fill all the required form boxes in MTD_TRIGGER_INTERVAL.");
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

      console.log(json_string);
      return added > 0 ? json_string : null;
    },
    triggerConversion(floatStr){
      const floatArray = floatStr.split(',').map(value => parseFloat(value.trim()));
      return floatArray
    },
    toggleInstructions(){
      this.showInstructions = !this.showInstructions;
    },
    addGraph(){
      const paramSelect = document.getElementById('param');

      if(paramSelect.options.length >=5){
        alert("You can only add up to 5 graphs.");
        return;
      }

      const newOption = document.createElement('option');
      newOption.text = `Graph ${paramSelect.options.length + 1}`;
      newOption.value = `graph${paramSelect.options.length + 1}`;

      paramSelect.appendChild(newOption);

      this.schemeGraph = newOption.value;
   }
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
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: 2px solid #000; 
    position: relative;
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
  margin:10px 0 1em 0;
  width: 100%;
  text-align: center;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.advanced:hover{
  background-color: #3454a4;
  color: #ffffff;
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
  max-width: 100%;
  margin-bottom: 20px; 
  background: #ffffff;
  padding: 2em;
  border-radius: 10px;
  margin:2em;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 2px solid #000; 
  position: relative;
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
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
  background-color: #333;
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
  cursor: pointer;
  padding: 0 5px;
  display: inline-block;
}

.tooltip-container .tip {
  position: absolute;
  top: 0;
  left: 100%;
  display: none;
  min-width: 200px;
  padding: 8px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.tooltip-container:hover .tip{
  display: block;
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
    background-color: #000;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
 }

 .instructions:hover{
  background-color: #333;
 }

 .instruction-box {
    width: 100%;
    margin: 2em;
    margin-top: 0;
    padding: 2em;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
  background-color: #000;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
 }

 .addGraph:hover{
  background-color: #333;
}
</style>