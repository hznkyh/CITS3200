<template>
  <div class="button-container">
    <button class="png-btn" @click="getImageURL('network')">Network</button>
    <button class="png-btn" @click="getImageURL('mtd_record')">MTD Record</button>
    <button class="png-btn" @click="getImageURL('attack_record')"> Attack Record</button>
    <button class="png-btn" @click="getImageURL('attack_action')">Attack Action</button>
  </div>

  <div class="pngs" v-if="activePng">
    <img class="png" :src=imageURL alt="Network">
  </div>
</template>

<script>
export default {
    name: 'Metrics',
    data(){
        return{
            activePng: false,
            imageURL: null
        };
    },

    props: {
        sim_num : Number,
    },

    methods: {
      // getImageURL(type){
      //   this.imageURL = `http://localhost:8000/statistics/${this.sim_num}/${type}`
      //   console.log(this.imageURL)
      // }

      getImageURL(type){
        if(this.activePng === true){
          this.activePng = false;
          // this.imageURL = null;
        } else {
          this.activePng = true;
          this.imageURL = `http://localhost:8000/statistics/${type}`
          console.log(this.imageURL)
        }
      }
    },
};
</script>

<style>
  .png-box {
      width: 100%; 
      margin: 2em 0;
      padding: 2em;
      background-color: #ffffff;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .button-container{
    display: flex;
    justify-content: space-between;
    margin: 1em 2em;
  }

  .png-btn{
    width: 100%;
    background-color: #000;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
    margin-right: 10px;
  }

  .png-btn:hover{
    background-color: #333;
  }

  .pngs{
    width: 100%; 
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

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