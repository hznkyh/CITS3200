import { createApp } from 'vue'
import VNetworkGraph from "v-network-graph"
import "v-network-graph/lib/style.css"
import App from './App.vue'

import Home from './components/Home.vue'
import MTDSimulator from './components/MTDSimulator.vue'

import axios from 'axios'
axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/'

const app = createApp(App)
app.component('home', Home)
app.component('mtd-simulator', MTDSimulator)
app.use(VNetworkGraph)
app.mount('#app')

