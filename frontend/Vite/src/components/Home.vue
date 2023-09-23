<template>
  <div class="container">
    <div class="row">
      <div class="col"></div>
      <div class="col">
        <h1 class="heading">Moving</h1>
        <h1 class="heading">Target</h1>
        <h1 class="heading">Defence</h1>
      </div>
      <div class="col"></div>
    </div>
  </div>
  <div class="row">
    <div class="col"></div>
    <div class="col">
      <h1 class="description">Description</h1>
    </div>
    <div class="col"></div>
  </div>
  <p>This is a test sentence.</p>
  <p>This is a test sentence.</p>
  <p>This is a test sentence.</p>
  <p>This is a test sentence.</p>
  <p>This is a test sentence.</p>
  <p>This is a test sentence.</p>

  <!-- test getting data from backend -->
  <button @click="getMessage">Get from backend</button>
  <button @click="sendMessage">Send to backend</button>
    <p>{{ msg }}</p> 
</template>

<script>
  import axios from "axios";
  export default {
    name: 'Home',
    data() {
        return {
          msg: "你好，世界！",
        };
      },
      methods: {  
        getMessage() {
          axios.get("/").then((res) => {
            this.msg = res.data;        
          });
        },   
        sendMessage () { 
          axios.post(
            "/update_item/",
            {name: "Hank", age:20},
          ).then((res) => {
            console.log(res.data);
        }); 
      },
    }
  }
</script>

<style>
</style>