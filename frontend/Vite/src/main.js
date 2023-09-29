import { createApp } from 'vue'
import VNetworkGraph from "v-network-graph"
import "v-network-graph/lib/style.css"
import App from './App.vue'

import Home from './components/Home.vue'
import MTDSimulator from './components/MTDSimulator.vue'

import axios from 'axios'

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/'

const session = await fetch("http://127.0.0.1:8000/uuid").then((response) => response.json()).then((data) => data)

const token = await axios.post("/token", {
    grant_type: null,
    username: session,
    password: session,
    scope: null,
    client_id: null,
    client_secret: null,
}).then((response) => response.json()).then((data) => data);

console.log('token',token);
axios.defaults.headers.common = {
    Authorization: `Bearer ${token}`
}

const app = createApp(App)
app.component('home', Home)
app.component('mtd-simulator', MTDSimulator)
app.use(VNetworkGraph)
app.mount('#app')


