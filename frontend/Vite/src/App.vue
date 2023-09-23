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
  <footer>
    <p>&copy; 2023 Semester 1 CITS3200 Project</p>
  </footer>
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
  padding: 30px;
  text-align: center;
  font-size: 35px;
  color: white;
}
footer {
  text-align: center;
  padding: 1em 0 0.5em 0;
  color: white;
  background-color: rgb(33,33,33);
}
</style>
