Vue.component('header-component', {
  template: `
            <div class="navigation">
              <a id="nav_home" class="active" href="main.html">Home</a>
              <a id="nav_simulator" class="inactive" href="simulator.html">Simulator</a>
            </div>
            `
});

var vm = new Vue({
  el: '#app',
})