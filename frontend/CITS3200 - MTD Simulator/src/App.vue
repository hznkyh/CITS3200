<template>
  <div class="navbar">
    <img class="logo" src="CITS3200\CITS3200 - MTD Simulator\src\components\icons\logo.jpg">
    <button @click="toggleComponent">Home</button>
    <button @click="toggleComponent">Simulator</button>
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
    toggleComponent() {
      this.currentView = this.currentView === 'Home' ? 'MTDSimulator' : 'Home';
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
  
  .navbar {
    width: 100%;
    background-color: #173590;
    overflow: auto;
  }

  button {
    float: left;
    display: block;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
    font-size: 17px;
    border: none;
    cursor: pointer;
  }

  @media screen and (max-width: 500px) {
    .navbar a {
      float: none;
      display: block;
    }
  }

  .logo{
    height: auto;
    width: auto;
    float: left;
    padding-left: 2%;
    margin: 0 auto;
    padding-right: 20px;
  }
</style>
