<template>
  <nav class="navbar navbar-expand-sm">
    <div class="container-fluid">
      <ul class="navbar-nav">
        <a class="navbar-brand" href="#">
          <img src="@/assets/logo.png" alt="UWA Logo" style="width:30px;" class="">  
        </a>
        <li class="nav-item">
          <a class="nav-link" href="#" @click="toggleHome">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" @click="toggleSimulator">Simulator</a>
        </li>
      </ul>
    </div>
  </nav>
  <component :is="currentView"/>
  <footer></footer>
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
header {
  background-color: rgb(12, 69, 225);
  padding: 30px;
  text-align: center;
  font-size: 35px;
  color: white;
}
footer {
  flex-shrink: 0;
  background-color: #777;
  text-align: center;
  color: white;
  bottom: 0;
  padding: 10px;
}
</style>
