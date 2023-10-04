<template>
  <div class="button-container">
    <button class="png-btn" @click="togglePng('png1')">Network</button>
    <button class="png-btn" @click="togglePng('png2')">MTD Record</button>
    <button class="png-btn" @click="togglePng('png3')"> Attack Record</button>
    <button class="png-btn" @click="togglePng('png4')">Attack Action</button>
  </div>

  <div class="pngs">
    <img class="png" src="http://localhost:8000/statistics/network" alt="Network" v-if="activePng === 'png1'">
    <img class="png" src="http://localhost:8000/statistics/mtd_record" alt="MTD Record" v-if="activePng === 'png2'">
    <img class="png" src="http://localhost:8000/statistics/attack_record" alt="Attack Record" v-if="activePng === 'png3'">
    <img class="png" src="http://localhost:8000/statistics/attack_action" alt="Attack Action" v-if="activePng === 'png4'">
  </div>
</template>

<script>
export default {
    name: 'Metrics',
    data(){
        return{
            activePng: null,
            imageURL: null
        };
    },

    props: {
        sim_num : Number,
    },

    methods: {
      togglePng(png){
        // console.log(this.sim_num)
        if(this.activePng === png){
            this.activePng = null;
        } else {
            this.activePng = png;
        }
      },
    },
};

</script>

<style>
  .button-container{
    display: flex;
    justify-content: space-between;
    margin: 1em 2em;
  }

  .png-btn{
    border: 1px solid black;
    border-radius: 15px;
    background-color: white;
    color: black;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
  }

  .png-btn:hover{
    background-color: black;
    color: white;
  }

  .pngs{
    max-width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 20px;
    max-width: fit-content;
  }

  .png {
    max-width: 100%;
    max-height: 100%;
  }
</style>