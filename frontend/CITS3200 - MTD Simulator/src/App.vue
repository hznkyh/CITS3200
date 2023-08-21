<template>
  <div class="navbar">
    <img class="logo" src="@/assets/logo.png">
    <button @click="toggleHome">Home</button>
    <button @click="toggleSimulator">Simulator</button>
  </div>
  <component :is="currentView"/>
</template>

<script>
import Home from './components/Home.vue';
import MTDSimulator from './components/MTDSimulator.vue';

export default {
  data() {
    return {
      currentView: 'Home' // Initial component name
    };
  },
  methods: {
    toggleHome() {
      this.currentView = 'Home';
    },
    toggleSimulator() {
      this.currentView = 'MTDSimulator';
    }
  },
  components: {
    Home,
    MTDSimulator
  }
};
</script>

<style>
  body{
    margin: 0;
  }

  .logo{
    height: 30px;
    width: 30px;
    float: left;
    margin: 10px;
  }
  
  .navbar {
    overflow: hidden;
    background-color: #333;
    top: 0;
    width: 100%;
    z-index: 1;
  }

  button {
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
    border: none;
    background-color: inherit;
    font-size: 17px;
    margin-right: 2%;
  }

  button:hover {
    background-color: #ddd;
    color: black;
  }

  @media screen and (max-width: 500px) {
    .logo{
      height: auto;
      width: auto;
      float: left;
      padding-left: 2%;
      margin: 0 auto;
      padding-right: 20px;
    }
  }
</style>
