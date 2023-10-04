<template>
  <div class="png">
    <div class="row">
        <button class="btn" @click="togglePng('png1')">Network</button>
        <button class="btn" @click="togglePng('png2')">MTD Record</button>
        <button class="btn" @click="togglePng('png3')"> Attack Record</button>
        <button class="btn" @click="togglePng('png4')">Attack Action</button>
      </div>
  </div>
  <div class="png-box">
    <img src="http://localhost:8000/statistics/network" alt="Network" />
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

    methods: {
      togglePng(png){
        if(this.activePng === png){
            this.activePng = null;
        } else {
            this.activePng = png;
        }
      },
      getNetwork() {
        this.imageURL = 'http://localhost:8000/statistics/network';
      }
    },
};

</script>

<style>
.btn {
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

.row{
  /* display: flex; */
  justify-content: space-between;
  margin-bottom: 15px;
}
.group:last-child{
    margin-right: 0;
}

.png-box {
    width: 100%; 
    margin: 2em 0;
    padding: 2em;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>