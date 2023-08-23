Vue.component('home-header-component', {
  template: `
            <div class="navigation">
              <a id="nav_home" class="active" href="main.html">Home</a>
              <a id="nav_simulator" class="inactive" href="simulator.html">Simulator</a>
            </div>
            `
});

Vue.component('simulator-header-component', {
  template: `
            <div class="navigation">
              <a id="nav_home" class="inactive" href="main.html">Home</a>
              <a id="nav_simulator" class="active" href="simulator.html">Simulator</a>
            </div>
            `
});

var vm = new Vue({
  el: '#app',
})