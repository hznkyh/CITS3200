import { createApp } from 'vue'
import VNetworkGraph from "v-network-graph"
import "v-network-graph/lib/style.css"
import App from './App.vue'

import Home from './components/Home.vue'
import MTDSimulator from './components/MTDSimulator.vue'

import axios from 'axios'

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/'

const session = await axios.get("http://localhost:8000/uuid").then((data) => data.data)
//console.log('session',session);

const params = new URLSearchParams();
params.append('username', session);
params.append('password', session);

const token = await axios.post("http://localhost:8000/token", params).then((data) => data.data.access_token)

//console.log('token',token);
axios.defaults.headers.common = {
    Authorization: `Bearer ${token}`
}

const app = createApp(App)
app.component('home', Home)
app.component('mtd-simulator', MTDSimulator)
app.use(VNetworkGraph)
app.mount('#app')


