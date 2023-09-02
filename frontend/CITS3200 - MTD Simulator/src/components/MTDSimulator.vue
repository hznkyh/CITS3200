<template>
  <div id="web">
    <header>
      <h2>MTD Simulator</h2>
    </header>

  <div id="container">
    <section class="content">
        <div class="panel">
          <form class="paramForm" v-on:submit.prevent="submitForm" >
            <h2> Parameters Panel</h2>

            <label>Number of Nodes: </label>
            <input id="param" type="text" placeholder="Number of Nodes..." v-model="nodeNumber">

            <label>Number of Nodes: </label>
            <input id="param" type="text" placeholder="Number of Nodes..." v-model="node1">

            <label>Number of Nodes: </label>
            <input id="param" type="text" placeholder="Number of Nodes..." v-model="node2">

            <label>Number of Nodes: </label>
            <input id="param" type="text" placeholder="Number of Nodes..." v-model="node3">

            <label>Number of Nodes: </label>
            <input id="param" type="text" placeholder="Number of Nodes..." v-model="node4">

            <button class="advanced" @click="toggleAdvanced()">Advanced</button>
            <div id="advancedPanel" class="hidden">
              <label>Number of Nodes: </label>
              <input id="param" type="text" placeholder="Number of Nodes..." v-model="node5">
              <label>Number of Nodes: </label>
              <input id="param" type="text" placeholder="Number of Nodes..." v-model="node6">
              <label>Number of Nodes: </label>
              <input id="param" type="text" placeholder="Number of Nodes..." v-model="node7">
            </div>

            <input type="submit" value="Submit">

            </form>
        </div>
        <article>
          <h1>Network Display</h1>
          <network></network>
        </article>
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
}

.panel{
  float: left;
  width: 30%;
  background: #ccc;
  padding: 20px;
  overflow: auto;
  max-height: calc(100vh - 10px);
}

.advanced {
  border: 0px;
  background-color: #ccc;
  display: inline-block;
  margin: 0;
}

.hidden{
  display: none;
}

article {
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
  overflow: auto;
}

@media (max-width: 600px) {
  form, article {
    width: 100%;
    height: auto;
  }
}

</style>