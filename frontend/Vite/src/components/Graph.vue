<script lang="ts">
    import axios from "axios";
    import { reactive, ref } from "vue"
    import * as vNG from "v-network-graph"
    import { Nodes, Edges, Layouts } from "v-network-graph"
    import data from "./data"
    import data2 from "./data2"
    import data3 from "./data3"
    import data4 from "./data4"
    import data5 from "./data5"

    import nodeInfo from "./NodeInfo.vue"
    import Metrics from "./Metrics.vue"

    import {
        ForceLayout,
        ForceNodeDatum,
        ForceEdgeDatum,
    } from "v-network-graph/lib/force-layout"

    var msgs: string [] = ['', '', '', '', ''];

    const graph = ref<vNG.VNetworkGraphInstance>()
    const selectedNodes = ref<string[]>([])

    const graph2 = ref<vNG.VNetworkGraphInstance>()
    const selectedNodes2 = ref<string[]>([])

    const graph3 = ref<vNG.VNetworkGraphInstance>()
    const selectedNodes3 = ref<string[]>([])

    const graph4 = ref<vNG.VNetworkGraphInstance>()
    const selectedNodes4 = ref<string[]>([])

    const graph5 = ref<vNG.VNetworkGraphInstance>()
    const selectedNodes5 = ref<string[]>([])

    var nodes = [reactive({ ...data.nodes }), reactive({ ...data2.nodes }), reactive({ ...data3.nodes }), reactive({ ...data4.nodes }), reactive({ ...data5.nodes })]
    var edges = [reactive({ ...data.edges }), reactive({ ...data2.edges }), reactive({ ...data3.edges }), reactive({ ...data4.edges }), reactive({ ...data5.edges })]
    var layouts = [reactive({ ...data.layouts }), reactive({ ...data2.layouts }), reactive({ ...data3.layouts }), reactive({ ...data4.layouts }), reactive({ ...data5.layouts })]
    var number_of_sims = 0;
    var simNames: string [] = [];

    var graphIndex: number[] = [-1, -1, -1, -1, -1];
    var startSim: boolean[] = [false, false, false, false, false];
    var storedGraph = {}
    var number_of_graphs: number[] = [];
    var exposed: string[] = [];
    var old_subnets = {}

    var intervalIDs: number[] = [];

    function clearData() {
        for (var i = 0; i < nodes.length; i++) {
            var node = nodes[i]
            var edge = edges[i]
            var layout = layouts[i]
            for (var key in node) {
                delete node[key]
            }
            for (var key in edge) {
                delete edge[key]
            }
            for (var key in layout) {
                layout[key] = {}
            }
        }

        number_of_graphs = [];
        graphIndex = [-1, -1, -1, -1, -1];
        startSim = [false, false, false, false, false];

        for (var i = 0; i < intervalIDs.length; i++) {
            clearInterval(intervalIDs[i])
        }
    }

    function findExposed(id, nodeId: string) {
        for (var key in edges[id]) {
            var edge = edges[id][key]
            if (edge.source == nodeId) {
                exposed.push(edge.target)
            }
        }
    }

    function generateCoordinates(
        numCoordinates: number,
        minDistance: number
        ): [number, number][] {
        var coordinates: [number, number][] = [];
        
        while (coordinates.length < numCoordinates) {
            const x = Math.random() * (600 - (-600)) + (-600); // Adjust the range as needed
            const y = Math.random() * (350 - (-350)) + (-350); // Adjust the range as needed

            // Check if the new coordinates satisfy the minimum distance requirement
            const valid = coordinates.every(([x1, y1]) => {
                return Math.abs(x - x1) >= minDistance && Math.abs(y - y1) >= minDistance;
                // return Math.abs(x - x1) >= minDistance
            });
            if (valid) {
            coordinates.push([x, y]);
            }
        }

        return coordinates;
    }

    function layout(id) {
        // layout the nodes based on their subnet
        var new_subnets = {}

        for (var key in nodes[id]) {
            var node = nodes[id][key]
            var subnet = node.subnet
            var layer = node.layer
            var location = `${subnet}-${layer}`
            if (location in new_subnets) {
                new_subnets[location].push(key)
            } else {
               new_subnets[location] = [key]
            }
        }
        if (JSON.stringify(new_subnets) == JSON.stringify(old_subnets)) {
            return
        }

        var coordinates = generateCoordinates(Object.keys(new_subnets).length, 60)

        var index = 0
        for (var key in new_subnets) {
            var subnet = new_subnets[key]
            var centerx = coordinates[index][0]
            var centery = coordinates[index][1]
            var subnetSize = subnet.length
            var subnetRadius = 30
            var angle = 360 / subnetSize
            var angleIndex = 0
            for (var i = 0; i < subnetSize; i++) {
                var x = centerx + subnetRadius * Math.cos(angleIndex * angle * Math.PI / 180) 
                var y = centery + subnetRadius * Math.sin(angleIndex * angle * Math.PI / 180) 
                layouts[id].nodes[subnet[i]] = { x, y }
                angleIndex++
            }
            index++
        }
        old_subnets = new_subnets
    }

    export default {
        name: 'Network',
        components: {
            vNG,
            nodeInfo,
            Metrics,
        },
        methods: {
            async getGraph() {
                try {
                    clearData();
                    const response = await axios.get("/network/multi-graph");
                    storedGraph = response.data;
                    for (let key in storedGraph) {
                        number_of_graphs.push(storedGraph[key].length)
                    }
                    this.drawAll();
                } catch (error) {
                    //console.error(error);
                }
            },

            start(id) {
                if (!startSim[id]) {
                    startSim[id] = true
                    this.togglePlay(id, true)
                    this.msgs[id] = "Simulation started"
                    intervalIDs[id] = setInterval(() => {
                        if (startSim[id]) {
                            // this.msg = "Running"
                            graphIndex[id]++
                            if (graphIndex[id] >= number_of_graphs[id]) {
                                startSim[id] = false
                                this.togglePlay(id, false)
                                this.msgs[id] = "Simulation finished."
                                clearInterval(intervalIDs[id])
                                return
                            }
                            this.step(id)
                        }
                    }, 1500)
                }
            },

            stop(id) {
                startSim[id] = false
                this.togglePlay(id, false)
                this.msgs[id] = "Simulation stopped."

            },
            drawAll(){ 
                var graphs = [graph,graph2,graph3,graph4,graph5]
                for (var i = 0; i < number_of_sims;i++){ 
                    if(graphIndex[i] == -1) {
                        graphIndex[i] = 0;
                        this.step(i);
                    }
                    this.step(i);
                }
            },
            manualStep(id, direction) {
                clearInterval(intervalIDs[id])
                startSim[id] = false
                this.togglePlay(id, false)


                this.msgs[id] = "Simulation stopped."
                if (direction == "back") {
                    graphIndex[id] = graphIndex[id] - 1
                    if (graphIndex[id] < 0) {
                        graphIndex[id] = 0

                        this.msgs[id] = "This is the first state."

                    }
                }
                if (direction == "forward") {
                    graphIndex[id] = graphIndex[id] + 1
                    if (graphIndex[id] >= number_of_graphs[id]) {
                        graphIndex[id] = number_of_graphs[id] - 1
                        this.msgs[id] = "This is the last state."
                    }
                }
                this.step(id)

                // this.msg = "Stopped"
            },

            step(id) {
                exposed = [];
                var graph
                try {
                    graph = storedGraph[simNames[id]][graphIndex[id]]
                }
                catch (error) {
                    this.msgs[id] = "Simulation not ready"
                    startSim[id] = false
                    this.togglePlay(id, false)
                    return
                }

                var number_of_edges = graph.links.length;
                var nextEdgeIndex = 1
                for (var z = 0; z < number_of_edges; z++) {
                    const edgeId = `edge${nextEdgeIndex}`
                    const source = `node${graph.links[z].source + 1}`
                    const target = `node${graph.links[z].target + 1}`
                    edges[id][edgeId] = { source, target }
                    nextEdgeIndex++
                };

                var nextNodeIndex = 1
                for (var j = 0; j < graph.nodes.length; j++) {
                    var node = graph.nodes[j]
                    const nodeId = `node${node.id + 1}`
                    const name = `N${nextNodeIndex}`
                    var subnet = node.subnet
                    var layer = node.layer
                    var color = ''
                    if (node.host.compromised == true) {
                        color = `red`
                        findExposed(id, nodeId)
                    } else if (exposed.includes(nodeId)) {
                        color = `yellow`
                    }
                    else {
                        color = `green`
                    }
                    var host = node.host
                    nodes[id][nodeId] = {color, subnet, layer, host}
                    nextNodeIndex++
                }
                layout(id)
                // const graphComponent = this.$refs.graph;
                // // Call the fitToContents method of the component
                // graphComponent.fitToContents();
            },

            toggleNodeInfo(id, display) {
                switch (id) {
                    case 1:
                        this.showNodeInfo = display
                        break;
                    case 2:
                        this.showNodeInfo2 = display
                        break;
                    case 3:
                        this.showNodeInfo3 = display
                        break;
                    case 4:
                        this.showNodeInfo4 = display
                        break;
                    case 5:
                        this.showNodeInfo5 = display
                        break;
                    default:
                        // Handle other cases or set a default behavior
                        break;
                }
            },

            handleLabel(id) {
                switch(id) {
                    case "graph1":
                        this.showGraph = !this.showGraph
                        break;
                    case "graph2":
                        this.showGraph2 = !this.showGraph2
                        break;
                    case "graph3":
                        this.showGraph3 = !this.showGraph3
                        break;
                    case "graph4":
                        this.showGraph4 = !this.showGraph4
                        break;
                    case "graph5":
                        this.showGraph5 = !this.showGraph5
                        break;
                    default:
                        // Handle other cases or set a default behavior
                        break;
                }
            },

            revealLabel(number) {

                switch (number) {
                    case 0:
                        this.showLabel1 = false;
                        this.showLabel2 = false;
                        this.showLabel3 = false;
                        this.showLabel4 = false;
                        this.showLabel5 = false;
                        break;
                    case 1:
                        this.showLabel1 = true;
                        this.showLabel2 = false;
                        this.showLabel3 = false;
                        this.showLabel4 = false;
                        this.showLabel5 = false;
                        break;
                    case 2:
                        this.showLabel1 = true;
                        this.showLabel2 = true;
                        this.showLabel3 = false;
                        this.showLabel4 = false;
                        this.showLabel5 = false;
                        break;
                    case 3:
                        this.showLabel1 = true;
                        this.showLabel2 = true;
                        this.showLabel3 = true;
                        this.showLabel4 = false;
                        this.showLabel5 = false;
                        break;
                    case 4:
                        this.showLabel1 = true;
                        this.showLabel2 = true;
                        this.showLabel3 = true;
                        this.showLabel4 = true;
                        this.showLabel5 = false;
                        break;
                    case 5:
                        this.showLabel1 = true;
                        this.showLabel2 = true;
                        this.showLabel3 = true;
                        this.showLabel4 = true;
                        this.showLabel5 = true;
                        break;
                    default:
                        // Handle other cases or set a default behavior
                        break;
                }
            },
            addGraph() {
                if (number_of_sims < 5) {
                    this.isPopupOpen = true;
                }
            },
            removeGraph() {
                if (number_of_sims >= 0) {
                    switch (number_of_sims) {
                        case 1:
                            this.showGraph = false;
                            break;
                        case 2:
                            this.showGraph2 = false;
                            break;
                        case 3:
                            this.showGraph3 = false;
                            break;
                        case 4:
                            this.showGraph4 = false;
                            break;
                        case 5:
                            this.showGraph5 = false;
                            break;
                    }
                    number_of_sims--
                }
                this.revealLabel(number_of_sims)
            },
            remove(sim_num){ 
                var graphName = simNames[sim_num]
                this.$emit('removeGraph',graphName)
                simNames.splice(sim_num, 1);
                graphIndex.splice(sim_num, 1);
                graphIndex.push(-1)
                delete storedGraph[graphName] 
                delete simNames[graphName]
                startSim = [false, false, false, false, false];

                for (var i = 0; i < intervalIDs.length; i++) {
                    clearInterval(intervalIDs[i])
                }
                this.removeGraph(graphName);
                this.drawAll();
            },
            closePopup() {
                this.userInput = '';             
                this.isPopupOpen = false;         
            },
            submitPopup() {
                // Check if userInput is longer than 20 characters
                if (this.userInput.length > 20) {
                    this.errorMessage = 'Input should be a maximum of 20 characters.';
                // Check if name is already used
                } else if (this.userInput.length == 0){
                    this.errorMessage = 'Input should be at least one character.';
                } else if (simNames.includes(this.userInput)) {
                    this.errorMessage = 'Names already used.';
                }   
                else {
                    number_of_sims++;
                    this.errorMessage = '';  // Clear any previous error messages
                    this.isPopupOpen = false;
                    simNames.push(this.userInput);
                    this.$emit('addGraph', this.userInput);
                    this.userInput = '';

                    this.revealLabel(number_of_sims);
                }
            },

            togglePlay(id, state) {
                switch (id) {
                    case 0:
                        this.isPlaying = state
                        break;
                    case 1:
                        this.isPlaying2 = state
                        break;
                    case 2:
                        this.isPlaying3 = state
                        break;
                    case 3:
                        this.isPlaying4 = state
                        break;
                    case 4:
                        this.isPlaying5 = state
                        break;
                }
            },
        },
        data() {
            return {
                nodes,
                edges,
                layouts,
                isPopupOpen: false,
                userInput: '',
                errorMessage: '',
                simNames,
                msgs,

                graph,
                selectedNodes,
                showNodeInfo: false,
                showLabel1: false,
                showGraph:false,
                propNode:null,
                isPlaying: false,

                graph2,
                selectedNodes2,
                showNodeInfo2: false,
                showLabel2: false,
                showGraph2: false,
                propNode2:null,
                isPlaying2: false,

                graph3,
                selectedNodes3,
                showNodeInfo3: false,
                showLabel3: false,
                showGraph3: false,
                propNode3:null,
                isPlaying3: false,

                graph4,
                selectedNodes4,
                showNodeInfo4: false,
                showLabel4: false,
                showGraph4: false,
                propNode4:null,
                isPlaying4: false,

                graph5,
                selectedNodes5,
                showNodeInfo5: false,
                showLabel5: false,
                showGraph5: false,
                propNode5:null,
                isPlaying5: false,
            }
        },
        setup() {
            const nodeSize = 20

            const configs = reactive(vNG.defineConfigs({
                view: {
                    autoPanAndZoomOnLoad: "center-zero",
                    // onBeforeInitialDisplay: () => layout(),
                    autoPanOnResize: true,
                    scalingObjects: true,
                    minZoomLevel: 0.2,
                    maxZoomLevel: 1.5,
                    panEnabled: true,
                    zoomEnabled: true,
                    layoutHandler: new ForceLayout({
                        positionFixedByDrag: false,
                        positionFixedByClickWithAltKey: true,
                        createSimulation: (d3, nodes, edges) => {
                        // d3-force parameters
                        const forceLink = d3.forceLink<ForceNodeDatum, ForceEdgeDatum>(edges).id(d => d.id)
                        return d3
                            .forceSimulation(nodes)
                            .force("center", d3.forceCenter())
                            // .force("charge", d3.forceManyBody().strength(-100))
                            .force("collide", d3.forceCollide(nodeSize))
                            .alphaMin(0.001)
                        }
                    }),
                },
                node: {
                    normal: {
                        type: "circle", 
                        radius: nodeSize/2,
                        color: node => node.color,

                    },
                    label: { 
                        visible: false,
                    },

                    draggable: true,
                    selectable: 1,
                    selected: {
                        type: "circle",
                        color: "#4466cc",
                        radius: nodeSize/2,
                    },
                },
                edge: {
                    normal: {
                        color: "#aaa",
                        width: 3,
                    },
                    type: "straight",
                },
            }))
            return {
                nodeSize,
                configs,
                graph,
                graph2,
                graph3,
                graph4,
                graph5,
            }
        },
        watch: {
            selectedNodes(newVal, oldVal) {
                if (newVal[0]) {

                    if (nodes[0][newVal[0]].host) {
                        this.toggleNodeInfo(1, true)
                        var propNode = nodes[0][newVal[0]].host
                        this.propNode = propNode
                    }
                }
                else {
                    this.toggleNodeInfo(1, false)
                }
            },
            selectedNodes2(newVal, oldVal) {
                if (newVal[0]) {

                    if (nodes[1][newVal[0]].host) {
                        this.toggleNodeInfo(2, true)
                        var propNode = nodes[1][newVal[0]].host
                        this.propNode2 = propNode
                    }
                }
                else {
                    this.toggleNodeInfo(2, false)
                }
            },
            selectedNodes3(newVal, oldVal) {
                if (newVal[0]) {

                    if (nodes[2][newVal[0]].host) {
                        this.toggleNodeInfo(3, true)
                        var propNode = nodes[2][newVal[0]].host
                        this.propNode3 = propNode
                    }
                }
                else {
                    this.toggleNodeInfo(3, false)
                }
            },
            selectedNodes4(newVal, oldVal) {
                if (newVal[0]) {

                    if (nodes[3][newVal[0]].host) {
                        this.toggleNodeInfo(4, true)
                        var propNode = nodes[3][newVal[0]].host
                        this.propNode4 = propNode
                    }
                }
                else {
                    this.toggleNodeInfo(4, false)
                }
            },
            selectedNodes5(newVal, oldVal) {
                if (newVal[0]) {

                    if (nodes[4][newVal[0]].host) {
                        this.toggleNodeInfo(5, true)
                        var propNode = nodes[4][newVal[0]].host
                        this.propNode5 = propNode
                    }
                }
                else {
                    this.toggleNodeInfo(5, false)
                }
            },
        },
    }
</script>

<template>
    <button class="addGraph" @click="addGraph()">Add Simulation</button>
    <div v-if="isPopupOpen" class="popup">
    <div class="popup-content">
        <span class="close-icon" @click="closePopup">×</span>
        <input v-model="userInput" type="text" placeholder="Name of simulation">
        <p class="error-message">{{ errorMessage }}</p> 
        <button class="close-button" @click="submitPopup">Submit</button>
    </div>
    </div>
    <div id="sim1" class="sim-label" @click="handleLabel('graph1')" v-if="showLabel1"> 
        <span>{{simNames[0]}}</span>
        <div class="delete">
            <i class="bi bi-trash3" @click.stop="remove(0)"></i>
        </div>
    </div>
    <div id="graph1" class="graph-container" v-if="showGraph">
        <v-network-graph
        ref="graph"
        class="graph"
        v-model:selected-nodes="selectedNodes"
        :nodes="nodes[0]"
        :edges="edges[0]"
        :layouts="layouts[0]"
        :configs="configs"
        >
        </v-network-graph>
        <div class="graph-view">
            <div class="group">
                <i class="bi bi-arrows-fullscreen" @click="graph?.fitToContents()"></i>
            </div>
            <div class="group">
                <i class="bi bi-zoom-in" @click="graph?.zoomIn()"></i>
            </div>
            <div class="group">
                <i class="bi bi-zoom-out" @click="graph?.zoomOut()" ></i>
            </div>
        </div>
        <div class="control-panel">
            <i class="bi bi-skip-backward" @click="manualStep(0, 'back')"></i>
            <i class="bi bi-play" @click="start(0)" v-if="!isPlaying"></i>
            <i class="bi bi-pause" @click="stop(0)" v-if="isPlaying"></i>
            <i class="bi bi-skip-forward" @click="manualStep(0, 'forward')" ></i>
        </div>
        <p class="message"> {{msgs[0]}} </p>
        <div id="node-info" class="node-info" v-if="showNodeInfo" ref="nodeInfo">
            <nodeInfo :node="propNode"></nodeInfo>
        </div>
        <div>
            <Metrics :simName=simNames[0]></Metrics>
        </div>
    </div>

    <div id="sim2" class="sim-label" @click="handleLabel('graph2')" v-if="showLabel2"> 
        <span>{{simNames[1]}}</span>
        <i class="bi bi-trash3" @click.stop="remove(1)"></i>
    </div>
    <div id="graph2" class="graph-container" v-if="showGraph2">
        <v-network-graph 
        ref="graph2"
        class="graph"
        v-model:selected-nodes="selectedNodes2"
        :nodes="nodes[1]"
        :edges="edges[1]"
        :layouts="layouts[1]"
        :configs="configs"
        >
        </v-network-graph>
        <div class="graph-view">
            <div class="group">
                <i class="bi bi-arrows-fullscreen" @click="graph2?.fitToContents()"></i>
            </div>
            <div class="group">
                <i class="bi bi-zoom-in" @click="graph2?.zoomIn()"></i>
            </div>
            <div class="group">
                <i class="bi bi-zoom-out" @click="graph2?.zoomOut()" ></i>
            </div>
        </div>
        <div class="control-panel">
            <i class="bi bi-skip-backward" @click="manualStep(1, 'back')"></i>
            <i class="bi bi-play" @click="start(1)" v-if="!isPlaying2"></i>
            <i class="bi bi-pause" @click="stop(1)" v-if="isPlaying2"></i>
            <i class="bi bi-skip-forward" @click="manualStep(1, 'forward')" ></i>
        </div>
        <p class="message"> {{msgs[1]}} </p>
        <div id="node-info2" class="node-info" v-if="showNodeInfo2">
            <nodeInfo :node="propNode2"></nodeInfo>
        </div>
        <div>
            <Metrics :simName=simNames[1]></Metrics>
        </div>
    </div>
    <div id="sim3" class="sim-label" @click="handleLabel('graph3')" v-if="showLabel3"> 
        <span>{{simNames[2]}}</span>
        <i class="bi bi-trash3" @click.stop="remove(2)"></i>
    </div>
    <div id="graph3" class="graph-container" v-if="showGraph3">
        <v-network-graph 
        ref="graph3"
        class="graph"
        v-model:selected-nodes="selectedNodes3"
        :nodes="nodes[2]"
        :edges="edges[2]"
        :layouts="layouts[2]"
        :configs="configs"
        >
        </v-network-graph>
        <div class="graph-view">
            <div class="group">
                <i class="bi bi-arrows-fullscreen" @click="graph3?.fitToContents()"></i>
            </div>
            <div class="group">
                <i class="bi bi-zoom-in" @click="graph3?.zoomIn()"></i>
            </div>
            <div class="group">
                <i class="bi bi-zoom-out" @click="graph3?.zoomOut()" ></i>
            </div>
        </div>
        <div class="control-panel">
            <i class="bi bi-skip-backward" @click="manualStep(2, 'back')"></i>
            <i class="bi bi-play" @click="start(2)" v-if="!isPlaying3"></i>
            <i class="bi bi-pause" @click="stop(2)" v-if="isPlaying3"></i>
            <i class="bi bi-skip-forward" @click="manualStep(2, 'forward')" ></i>
        </div>
        <p class="message"> {{msgs[2]}} </p>
        <div id="node-info2" class="node-info" v-if="showNodeInfo3">
            <nodeInfo :node="propNode3"></nodeInfo>
        </div>
        <div>
            <Metrics :simName=simNames[2]></Metrics>
        </div>
    </div>
    <div id="sim4" class="sim-label" @click="handleLabel('graph4')" v-if="showLabel4"> 
        <span>{{simNames[3]}}</span>
        <i class="bi bi-trash3" @click.stop="remove(3)"></i>
    </div>
    <div id="graph4" class="graph-container" v-if="showGraph4">
        <v-network-graph 
        ref="graph4"
        class="graph"
        v-model:selected-nodes="selectedNodes4"
        :nodes="nodes[3]"
        :edges="edges[3]"
        :layouts="layouts[3]"
        :configs="configs"
        >
        </v-network-graph>
        <div class="graph-view">
            <div class="group">
                <i class="bi bi-arrows-fullscreen" @click="graph4?.fitToContents()"></i>
            </div>
            <div class="group">
                <i class="bi bi-zoom-in" @click="graph4?.zoomIn()"></i>
            </div>
            <div class="group">
                <i class="bi bi-zoom-out" @click="graph4?.zoomOut()" ></i>
            </div>
        </div>
        <div class="control-panel">
            <i class="bi bi-skip-backward" @click="manualStep(3, 'back')"></i>
            <i class="bi bi-play" @click="start(3)" v-if="!isPlaying4"></i>
            <i class="bi bi-pause" @click="stop(3)" v-if="isPlaying4"></i>
            <i class="bi bi-skip-forward" @click="manualStep(3, 'forward')" ></i>
        </div>
        <p class="message"> {{msgs[3]}} </p>
        <div id="node-info2" class="node-info" v-if="showNodeInfo4">
            <nodeInfo :node="propNode4"></nodeInfo>
        </div>
        <div>
            <Metrics :simName=simNames[3]></Metrics>
        </div>
    </div>
    <div id="sim5" class="sim-label" @click="handleLabel('graph5')" v-if="showLabel5"> 
        <span>{{simNames[4]}}</span>
        <i class="bi bi-trash3" @click.stop="remove(4)"></i>
    </div>
    <div id="graph5" class="graph-container" v-if="showGraph5">
        <v-network-graph 
        ref="graph5"
        class="graph"
        v-model:selected-nodes="selectedNodes5"
        :nodes="nodes[4]"
        :edges="edges[4]"
        :layouts="layouts[4]"
        :configs="configs"
        >
        </v-network-graph>
        <div class="graph-view">
            <div class="group">
                <i class="bi bi-arrows-fullscreen" @click="graph5?.fitToContents()"></i>
            </div>
            <div class="group">
                <i class="bi bi-zoom-in" @click="graph5?.zoomIn()"></i>
            </div>
            <div class="group">
                <i class="bi bi-zoom-out" @click="graph5?.zoomOut()" ></i>
            </div>
        </div>
        <div class="control-panel">
            <i class="bi bi-skip-backward" @click="manualStep(4, 'back')"></i>
            <i class="bi bi-play" @click="start(4)" v-if="!isPlaying5"></i>
            <i class="bi bi-pause" @click="stop(4)" v-if="isPlaying5"></i>
            <i class="bi bi-skip-forward" @click="manualStep(4, 'forward')" ></i>
        </div>
        <p class="message"> {{msgs[4]}} </p>
        <div id="node-info2" class="node-info" v-if="showNodeInfo5">
            <nodeInfo :node="propNode5"></nodeInfo>
        </div>
        <div>
            <Metrics :simName=simNames[4]></Metrics>
        </div>
    </div>
  </template>

<style>
    .graph-container {
        position:relative;
    }

    .graph {
        width: 100%;
        margin: 5px auto;
        height: 800px;
        margin-top: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 
        inset -2px -2px 5px rgba(255, 255, 255, 0.9), 
        inset 2px 2px 5px rgba(0, 0, 0, 0.2),
        -2px -2px 5px rgba(255, 255, 255, 0.9), 
        2px 2px 5px rgba(0, 0, 0, 0.2);
    }

    .hide {
        display: none;
    }

    .active {
        display: block;
    }

    .graph-view {
        position: absolute;
        top: 0.7em;
        left: 1em;
    }

    .node-info {
        position: absolute;
        top: 1em;
        right: 1em;
        border-radius: 15px;
        width: 20em;
        z-index: 1;
        margin: 2em;
        margin-top: 20px;
        padding: 1em;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 
        inset -2px -2px 5px rgba(255, 255, 255, 0.9), 
        inset 2px 2px 5px rgba(0, 0, 0, 0.2),
        -2px -2px 5px rgba(255, 255, 255, 0.9), 
        2px 2px 5px rgba(0, 0, 0, 0.2);
    }

    .node-info p {
        margin: 0.5em 0 0.5em 1em;
        padding: 0;
        text-align: left;
        font-size: 1em;
        color: black;
    }

    .sim-label {
        display: flex;
        justify-content: space-between;
        background-color: #3454a4;
        padding: 0.5em 1em;
        width: 100%;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 1em; 
        font-weight: 500;
        color: white;
    }

    .btncp{
        background-color: #ffffff;
        width: 100%;
        text-align: center;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition: background-color 0.3s ease, color 0.3s ease;
        font-weight: 500;
        margin-top: 10px;
    }

    .btncp:hover{
        background-color: #3454a4;
        color: #ffffff;
    }

    .row{
        display: flex;
        justify-content: center;
        margin-bottom: 0px;
    }

    .group{
        flex: 1;
    }

    .popup {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 2;
    }

    .popup-content {
        position: relative;
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .close-button {
        background-color: #2ccd00;
        color: white;
        border: none;
        margin-left: 1em;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
    }

    .close-button:hover {
        background-color: #27ab02;
    }

    .control-panel {
        justify-content: center;
        display: flex;
    }

    .control-panel i {
        margin: 1em;
    }

    .message {
        text-align: center;
        display: flex;
        align-items: center; 
        justify-content: center; 
        height: 100%; 
    }

    .close-icon{
        position: absolute;
        top: 5px;
        right: 5px;
        cursor: pointer;
        font-size: 18px;
        font-weight: bold;
        color: #333;
        background-color: #f5f5f5;
        border: none;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: background-color 0.2s;

        &:hover{
            background-color: #e0e0e0;
        }
    }

    .error-message {
        color: red;
        font-size: 12px;
        margin-top: 10px;
    }
</style>


