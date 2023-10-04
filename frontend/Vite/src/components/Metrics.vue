<template>
  <div class="button-container">
    <button class="png-btn" @click="getImageURL('network')">Network</button>
    <button class="png-btn" @click="getImageURL('mtd_record')">MTD Record</button>
    <button class="png-btn" @click="getImageURL('attack_record')"> Attack Record</button>
    <button class="png-btn" @click="getImageURL('attack_action')">Attack Action</button>
  </div>

  <div class="pngs">
    <img class="png" :src=imageURL alt="Network">
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
      // togglePng(png){
      //   // console.log(this.sim_num)
      //   if(this.activePng === png){
      //       this.activePng = null;
      //   } else {
      //       this.activePng = png;
      //   }
      // },
    
      // getImageURL(type){
      //   this.imageURL = `http://localhost:8000/statistics/${this.sim_num}/${type}`
      //   console.log(this.imageURL)
      // }

      getImageURL(type){
        this.imageURL = `http://localhost:8000/statistics/${type}`
        console.log(this.imageURL)
      }
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