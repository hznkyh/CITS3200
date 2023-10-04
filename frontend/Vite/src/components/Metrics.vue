<template>
    <div class="png">
        <div class="row">
            <div class="group">
                <button class="btn1" @click="togglePng('png1')">Network</button>
                <div class="png-box" v-if="pngStates.png1">
                    <h1>PNG</h1>
                </div>
            </div>
            <div class="group">
                <button class="btn2" @click="togglePng('png2')">MTD Record</button>
                <div class="png-box" v-if="pngStates.png2">
                    <h1>PNG</h1>
                </div>
            </div>
            <div class="group">
                <button class="btn3" @click="togglePng('png3')"> Attack Record</button>
                <div class="png-box" v-if="pngStates.png3">
                    <h1>PNG</h1>
                </div>
            </div>
            <div class="group">
                <button class="btn4" @click="togglePng('png4')">Attack Action</button>
                <div class="png-box" v-if="pngStates.png4">
                    <h1>PNG</h1>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Metrics',
    data(){
        return{
            pngStates: {
                png1: false,
                png2: false,
                png3: false,
                png4: false
            }
        };
    },

    methods: {
        togglePng(png){
            this.pngStates[png] = !this.pngStates[png];
        }
    }
};
</script>

<style>
.btn1, .btn2, .btn3, .btn4 {
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

.btn1:hover:hover, .btn2:hover:hover, .btn3:hover:hover, .btn4:hover:hover{
  background-color: #333;
}

.row{
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.group{
  flex: 1;
  padding: 0 10px;
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