<template>
  <div class="content">
    <div class="panel">
      <form id="paramForm" v-on:submit.prevent="submitForm" >
        <h2> Parameters Panel</h2>
        <div>
          <label>Number of Nodes *:</label>
          <span id="tooltip">
            <span class='info'>
              <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
            </span>
            <span class="tip">The number of nodes in the network (network size).</span>
          </span>
          <input id="param" type="text" placeholder="Number of Nodes..." v-model="nodeNumber" name="total_nodes" required>
        </div>
        
        <div>
          <label>Number of Exposed Nodes *: </label>
          <span id="tooltip">
            <span class='info'>
              <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
            </span>
            <span class="tip">The number of exposed nodes in the network.</span>
          </span>
          <input id="param" type="text" placeholder="Number of Exposed Nodes..." v-model="nodeExposed" name="total_endpoints" required>
        </div>

        <div>
          <label>Number of Layers *: </label>
          <span id="tooltip">
            <span class='info'>
              <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
            </span>
            <span class="tip">The number of layers in the network</span>
          </span>
          <input id="param" type="text" placeholder="Number of Layers..." v-model="layers" name="total_layers" required>
        </div>

        <div>
          <label>Compromise Ratio *: </label>
          <span id="tooltip">
            <span class='info'>
              <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
            </span>
            <span class="tip">The ratio number that will terminate the simulation if reached.</span>
          </span>
          <input id="param" type="text" placeholder="Compromise Ratio..." v-model="compromisedRatio" name="terminate_compromise_ratio" required>
        </div>

        <div>
          <label>Scheme *: </label>
          <span id="tooltip">
            <span class='info'>
              <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
            </span>
            <span class="tip">How the simulator will run. Chose from: random (default), simultaneous, alternative, single and none.</span>
          </span>
          <select id="param" type="text" placeholder="Scheme..." v-model="scheme" name="scheme" required>
            <option value="random">random</option>
            <option value="simultaneous"> simultaneous</option>
            <option value="alternative">alternative</option>
            <option value="single">single</option>
            <option value="none">none</option>
          </select>
        </div>

        <div>
          <label>MTD Interval *: </label>
          <span id="tooltip">
            <span class='info'>
              <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
            </span>
            <span class="tip">The time interval to trigger an MTD(s)</span>
          </span>
          <input id="param" type="text" placeholder="MTD Interval..." v-model="interval" name="mtd_interval" required>
        </div>

        <div>
          <label>Finish Time *: </label>
          <span id="tooltip">
            <span class='info'>
              <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
            </span>
            <span class="tip">How long the simulation should run for</span>
          </span>
          <input id="param" type="text" placeholder="Finish Time..." v-model="finishTime" name="finish_time" required>
        </div>

        <div>
          <label>Checkpoints *: </label>
          <span id="tooltip">
            <span class='info'>
              <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
            </span>
            <span class="tip">How often snapshots are taken of the simulation</span>
          </span>
          <input id="param" type="text" placeholder="Checkpoints..." v-model="checkpoints" name="checkpoints" required>
        </div>

        <p id="advanced" class="advanced" @click="toggleAdvanced()">Advanced</p>
        <div id="advancedPanel" class="hidden">
          <div>
          <label>Total Subnets: </label>
          <span id="tooltip">
            <span class='info'>
              <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
            </span>
            <span class="tip">The number of subnets</span>
          </span>
          <input id="param" type="text" placeholder="Total Subnets..." v-model="totalSubnets" name="total_subnets">
        </div>

        <div>
          <label>Target Layers: </label>
          <span id="tooltip">
            <span class='info'>
              <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
            </span>
            <span class="tip">How often snapshots are taken of the simulation</span>
          </span>
          <input id="param" type="text" placeholder="Target Layers..." v-model="targetLayers" name="target_layers">
        </div>

          <div>
            <span id="tooltip">
              <label id="heading">MTD Priority</label>
              <span class='info'>
                <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
              </span>
              <span class="tip">Below you have the choice to change the priority of options the defender has to avoid an attack. By default (leave empty) it is ordered 1-7 from top to bottom. If you wish
                to change the order please fill in the form.
              </span>
            </span>
          </div>

          <label>Complete Topology Shuffle: </label>
          <input id="param" type="text" placeholder="Complete Topology Shuffle..." name="CompleteTopologyShuffle" v-model="compTopoShuffle">

          <label>Host Topology Shuffle: </label>
          <input id="param" type="text" placeholder="Host Topology Shuffle..." name="HostTopologyShuffle" v-model="hostTopoShuffle">

          <label>IP Shuffle: </label>
          <input id="param" type="text" placeholder="IP Shuffle..." name="IPShuffle" v-model="ipShuffle">

          <label>OS Diversity: </label>
          <input id="param" type="text" placeholder="OS Diversity..." name="OSDiversity" v-model="osDiveristy">

          <label>Port Shuffle: </label>
          <input id="param" type="text" placeholder="Port Shuffle..." name="PortShuffle" v-model="portShuffle">

          <label>Service Diversity: </label>
          <input id="param" type="text" placeholder="Service Diversity..." name="ServiceDivesity" v-model="ServDiversity">

          <label>User Shuffle: </label>
          <input id="param" type="text" placeholder="User Shuffle..." name="UserShuffle" v-model="userShuffle">

          <div>
            <span id="tooltip">
              <label id="heading">MTD Trigger Interval</label>
              <span class='info'>
                <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
              </span>
              <span class="tip">When to trigger the chosen scheme
              </span>
            </span>
          </div>

          <label>Simultaneous: </label>
          <input id="param" type="text" placeholder="(value, value)" name="simultaneous" v-model="similtaneous">

          <label>Random: </label>
          <input id="param" type="text" placeholder="(value, value)" name="random" v-model="random">

          <label>Alternative: </label>
          <input id="param" type="text" placeholder="(value, value)" name="alternative" v-model="alternative">

        </div>

        <input type="submit" value="Submit">
        </form>
        <p class="message"> {{ msg }} </p>
    </div>
    <div class="network">
      <Graph></Graph>
    </div>
  </div>
  <div class="instructions">
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
      <li>Node ID</li>
      <li>Node Type</li>
      <li>Node State</li>
      <li>Node IP</li>
      <li>Node OS</li>
      <li>Node Services</li>
      <li>Node Users</li>
    </ul>
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
    };
  },

  methods: {
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
        {field: this.checkpoints, validator: this.validateFloatInputs, fieldName: 'Checkpoints'},
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
    validateRatio(value){
      const parsedValue = parseFloat(value)
      return !isNaN(parsedValue) && parsedValue <= 1.0;
    },
    validatePrioityInput(num){
      const parsedValue = parseFloat(num);
      return !isNaN(parsedValue) && parsedValue >= 0 && parsedValue <= 7 || num == '';
    },
    validateWord(word){
      const possibleWords = ['random', 'simultaneous', 'alternative', 'single', 'none'];
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
    }

  },
};
</script>

<style>
  * {
  box-sizing: border-box; 
}

#app{
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow: hidden;
}

.content{
  display: flex;
  flex: 1;
  min-height: 90vh;
  max-height: 90vh;
}

.panel{
  float: left;
  width: 30%;
  background: #ccc;
  padding: 2em;
  max-height: 100%;
  border-radius: 35px;
  margin:2em;
  overflow-y: scroll;
}

.panel::-webkit-scrollbar {
  border: 0;
}

.advanced {
  border: 0px;
  background-color: #ccc;
  display: inline-block;
  padding: 0;
  margin: 0 0 0.5em 0;
  width: 100%;
  text-align: left;
}

.hidden{
  display: none;
}

.network {
  float: left;
  padding: 20px;
  width: 70%;
  height: auto;
  text-align: center;
  /* border: 2px solid #ccc; */
  padding:0;
  margin:1em;
  margin-bottom: 6em;
}

input[type=text] {
   width: 100%;
   margin: 5px 0 10px 0;
   display: inline-block;
   border: none;
   background: #f1f1f1;
}

input[type=text]:focus {
   background-color: #ddd;
   outline: none;
}

@media (max-width: 600px) {
  form, article {
    width: 100%;
    height: auto;
  }
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
  font-style: Italic;
}

#tooltip .tip { 
     display: none; 
}

 #tooltip:hover .tip { 
    display: block;
    color: #514f4e;
    background: white;
    padding: 3px;
    border: 1px solid #514f4e;
    width: auto
 }

 #heading{
  font-size: 20px;
  color: black;
 }

 .instructions {
    margin: 2em;
    margin-top: 0;
    padding: 2em;
    border: 2px solid #ccc;
    border-radius: 35px;
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
</style>