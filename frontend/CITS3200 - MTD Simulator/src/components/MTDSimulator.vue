<template>
  <div id="web">
    <div id="container">
      <section class="content">
        <div class="panel">
          <form class="paramForm" v-on:submit.prevent="submitForm" >
            <h2> Parameters Panel</h2>
            <div>
              <label>Number of Nodes *:</label>
              <button id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                <span class="tip">Hello!</span>
              </button>
              <input id="param" type="text" placeholder="Number of Nodes..." v-model="nodeNumber" required>
            </div>
            
            <div>
              <label>Number of Exposed Nodes *: </label>
              <button id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
              </button>
              <input id="param" type="text" placeholder="Number of Exposed Nodes..." v-model="nodeExposed" required>
            </div>

            <div>
             <label>Number of Layers *: </label>
             <button id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
              </button>
              <input id="param" type="text" placeholder="Number of Layers..." v-model="layers" required>
            </div>

            <div>
              <label>Compromise Ratio *: </label>
              <button id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
              </button>
              <input id="param" type="text" placeholder="Compromise Ratio..." v-model="compromisedRatio" required>
            </div>

            <div>
              <label>Scheme *: </label>
              <button id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
              </button>
              <input id="param" type="text" placeholder="Scheme..." v-model="scheme" required>
            </div>

            <div>
              <label>MTD Interval *: </label>
              <button id="tooltip">
                <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
              </button>
              <input id="param" type="text" placeholder="MTD Interval..." v-model="interval" required>
            </div>

            <button class="advanced" @click="toggleAdvanced()">Advanced</button>
            <div id="advancedPanel" class="hidden">
              <div>
                <button id="tooltip">
                  <span class='info'>
                  <img src='https://s3.lightboxcdn.com/vendors/906a5d64-2cda-407f-a2d5-6cf94c06ddbe/uploads/274a7932-a0fd-4a89-9f58-a83cc44112ca/info.svg' width='15' height='15'>
                </span>
                </button>
                <h4>MTD Priority</h4>
              </div>

              <label>Complete Topology Shuffle: </label>
              <input id="param" type="text" placeholder="Complete Topology Shuffle..." v-model="compTopoShuffle">

              <label>Host Topology Shuffle: </label>
              <input id="param" type="text" placeholder="Host Topology Shuffle..." v-model="hostTopoShuffle">

              <label>IP Shuffle: </label>
              <input id="param" type="text" placeholder="IP Shuffle..." v-model="ipShuffle">

              <label>OS Diversity: </label>
              <input id="param" type="text" placeholder="OS Diversity..." v-model="osDiveristy">

              <label>Port Shuffle: </label>
              <input id="param" type="text" placeholder="Port Shuffle..." v-model="portShuffle">

              <label>Service Diversity: </label>
              <input id="param" type="text" placeholder="Service Diversity..." v-model="ServDiversity">

              <label>User Shuffle: </label>
              <input id="param" type="text" placeholder="User Shuffle..." v-model="userShuffle">

            </div>

            <input type="submit" value="Submit">

            </form>
        </div>
        <div class="network">
          <h1>Network</h1>
          <network></network>
        </div>
      </section>
    </div>
  </div>
    


</template>

<script>
import network from './Network.vue';

export default {
  name: 'MTDSimulator',
  components: {
    network,
  },
  data(){
    return{
      nodeNumber:'',
      node1:'',
      node2:'',
      node3:'',
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
      if(this.validateInput(this.nodeNumber) && this.validateInput(this.node1) 
        && this.validateInput(this.node2) && this.validateInput(this.node3)){
        console.log('All values are valid')
        console.log(this.nodeNumber, this.node1, this.node2, this.node3)
      }
      else{
        console.log('Invalid inputs have been detected')
      }
    },
    validateInput(value){
      const parsedValue = parseFloat(value);
      return !isNaN(parsedValue) && parsedValue >= 0;
    },
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

#container{
  flex: 1;
}

@media (max-width: 600px) {
  form, article {
    width: 100%;
    height: auto;
  }
}

#tooltip{
    text-align: center;
    background-color: transparent;
    border: 0px !important;
    width: auto;
    color: #666666;
    font-size: 14px;
}

button .info {
      text-decoration: underline;
     font-style: Italic;
}

button .tip { 
     display: none; 
}

button:hover .info {
      display: none;
 }

button:hover .tip { 
     display: inline;
     color: #222525;
 }
</style>