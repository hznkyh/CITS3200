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

    const graph = ref<vNG.VNetworkGraphInstance>()
    // var nodes: Nodes = reactive({ ...data.nodes })
    // var edges: Edges = reactive({ ...data.edges })
    // var layouts: Layouts = reactive({ ...data.layouts})
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
    var number_of_sims = 1;

    var graphIndex: number[] = [-1, -1, -1, -1, -1];
    var startSim: boolean[] = [false, false, false, false, false];
    var storedGraph = {}
    var number_of_graphs: number[] = [];
    // var msg = "Simulation not started"
    var exposed: string[] = [];
    var old_subnets = {}

    var intervalIDs: number[] = [];

    function clearData() {
        for (var i = 0; i < nodes.length; i++) {
            nodes[i] = reactive({})
            edges[i] = reactive({})
            layouts[i] = reactive({nodes: {},})
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
        console.log(nodes[id])
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
    
    function getSim(id) {
        switch (id) {
            case 1:
                return storedGraph['graph1']
            case 2:
                return storedGraph['graph2']
            case 3:
                return storedGraph['graph3']
            case 4:
                return storedGraph['graph4']
            case 5:
                return storedGraph['graph5']
        }
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
                    this.msg = "Getting graph...";
                    const response = await axios.get("/network/multi-graph");
                    storedGraph = response.data;
                    console.log(storedGraph);
                    for (var i = 1; i <= number_of_sims; i ++) {
                        number_of_graphs.push(storedGraph[`graph${i}`].length)
                    }
                    console.log (number_of_graphs)
                    // this.msg = "Got graph";
                } catch (error) {
                    console.error(error);
                }
            },

            start(id) {
                if (!startSim[id]) {
                    startSim[id] = true
                    this.msg = "Start"
                    intervalIDs[id] = setInterval(() => {
                        if (startSim[id]) {
                            // this.msg = "Running"
                            graphIndex[id]++
                            this.step(id)
                        }
                    }, 1500)
                }
            },

            stop(id) {
                startSim[id] = false
                this.msg = "Stopped"

            },

            manualStep(id, direction) {
                clearInterval(intervalIDs[id])
                startSim[id] = false
                if (direction == "back") {
                    if (graphIndex[id] == 0) {
                        return
                    }
                    graphIndex[id] = graphIndex[id] - 1
                }
                startSim[id] = false
                if (direction == "forward") {
                    graphIndex[id] = graphIndex[id] + 1
                    if (graphIndex[id] == number_of_graphs[id]) {
                        this.msg = "Simulation finished"
                        graphIndex[id] = graphIndex[id] - 1
                        return
                    }
                }
                this.step(id)
                // this.msg = "Stopped"
            },

            step(id) {
                if (graphIndex[id] == number_of_graphs[id]) {
                    this.msg = "Simulation finished"
                    startSim[id] = false
                    clearInterval(intervalIDs[id])
                    return
                }
                exposed = [];
                var graph = storedGraph[`graph${id+1}`][graphIndex[id]]
                console.log(id)

                var number_of_edges = graph.links.length;
                var nextEdgeIndex = 1
                for (var z = 0; z < number_of_edges; z++) {
                    const edgeId = `edge${nextEdgeIndex}`
                    const source = `node${graph.links[z].source + 1}`
                    const target = `node${graph.links[z].target + 1}`
                    edges[id][edgeId] = { source, target }
                    nextEdgeIndex++
                };
                console.log(edges)

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
                console.log("clicked")
                switch (number) {
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
                this.$emit('childData', "add graph");
                number_of_sims++;
                this.revealLabel(number_of_sims)
            }
        },
        data() {
            return {
                // msg,
                // os_type,
                // os_version,
                // host_ip,
                // host_id,
                // p_u_compromise,
                // total_users,
                // uuid,
                // total_services,
                // total_nodes,
                // compromised,
                // compromised_services,

                nodes,
                edges,
                layouts,

                graph,
                // nodes,
                // edges,
                // layouts,
                selectedNodes,
                showNodeInfo: false,
                showLabel1: true,
                showGraph:false,
                propNode:null,

                graph2,
                // nodes2,
                // edges2,
                // layouts2,
                selectedNodes2,
                showNodeInfo2: false,
                showLabel2: false,
                showGraph2: false,
                propNode2:null,

                graph3,
                // nodes3,
                // edges3,
                // layouts3,
                selectedNodes3,
                showNodeInfo3: false,
                showLabel3: false,
                showGraph3: false,
                propNode3:null,

                graph4,
                // nodes4,
                // edges4,
                // layouts4,
                selectedNodes4,
                showNodeInfo4: false,
                showLabel4: false,
                showGraph4: false,
                propNode4:null,

                graph5,
                // nodes5,
                // edges5,
                // layouts5,
                selectedNodes5,
                showNodeInfo5: false,
                showLabel5: false,
                showGraph5: false,
                propNode5:null,
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
                // nodes,
                // edges,
                // layouts,
                // selectedNodes,
                graph2,
                graph3,
                graph4,
                graph5,
            }
        },
        watch: {
            selectedNodes(newVal, oldVal) {
                if (newVal[0]) {
                    console.log(nodes[newVal[0]].host)
                    if (nodes[newVal[0]].host) {
                        this.toggleNodeInfo(1, true)
                        var propNode = nodes[newVal[0]].host
                        this.propNode = propNode
                    }
                }
                else {
                    this.toggleNodeInfo(1, false)
                }
            },
            selectedNodes2(newVal, oldVal) {
                if (newVal[0]) {
                    console.log(nodes[newVal[0]].host)
                    if (nodes[newVal[0]].host) {
                        this.toggleNodeInfo(2, true)
                        var propNode = nodes[newVal[0]].host
                        this.propNode2 = propNode
                    }
                }
                else {
                    this.toggleNodeInfo(2, false)
                }
            },
            selectedNodes3(newVal, oldVal) {
                if (newVal[0]) {
                    console.log(nodes[newVal[0]].host)
                    if (nodes[newVal[0]].host) {
                        this.toggleNodeInfo(3, true)
                        var propNode = nodes[newVal[0]].host
                        this.propNode3 = propNode
                    }
                }
                else {
                    this.toggleNodeInfo(3, false)
                }
            },
            selectedNodes4(newVal, oldVal) {
                if (newVal[0]) {
                    console.log(nodes[newVal[0]].host)
                    if (nodes[newVal[0]].host) {
                        this.toggleNodeInfo(4, true)
                        var propNode = nodes[newVal[0]].host
                        this.propNode4 = propNode
                    }
                }
                else {
                    this.toggleNodeInfo(4, false)
                }
            },
            selectedNodes5(newVal, oldVal) {
                if (newVal[0]) {
                    console.log(nodes[newVal[0]].host)
                    if (nodes[newVal[0]].host) {
                        this.toggleNodeInfo(5, true)
                        var propNode = nodes[newVal[0]].host
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
    <span id="sim1" class="sim-label" @click="handleLabel('graph1')" v-if="showLabel1">Simulation 1</span>
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
        <div class="control-panel">
            <button @click="graph?.fitToContents()" ref="myBtn" class="btn">Fit</button>
            <button @click="graph?.zoomIn()">Zoom In</button>
            <button @click="graph?.zoomOut()">Zoom Out</button>
            <button @click="getGraph()">Get</button>
            <button @click="start(0)">Start/Continue</button>
            <button @click="manualStep(0, 'forward')">Step</button>
            <button @click="manualStep(0, 'back')">Step Back</button>
            <button @click="stop(0)">Stop</button>
        </div>
        <!-- <p class="message"> {{ msg }} </p> -->
        <div id="node-info" class="node-info" v-if="showNodeInfo" ref="nodeInfo">
            <nodeInfo :node="propNode"></nodeInfo>
        </div>
        <div>
            <Metrics></Metrics>
        </div>
    </div>

    <span id="sim2" class="sim-label" @click="handleLabel('graph2')" v-if="showLabel2">Simulation 2</span>
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
        <div class="control-panel">
            <button @click="graph2?.fitToContents()" ref="myBtn">Fit</button>
            <button @click="graph2?.zoomIn()">Zoom In</button>
            <button @click="graph2?.zoomOut()">Zoom Out</button>
            <button @click="getGraph()">Get</button>
            <button @click="start(1)">Start/Continue</button>
            <button @click="manualStep(1, 'forward')">Step</button>
            <button @click="manualStep(1, 'back')">Step Back</button>
            <button @click="stop(1)">Stop</button>
        </div>
        <!-- <p class="message"> {{ msg }} </p> -->
        <div id="node-info2" class="node-info" v-if="showNodeInfo2">
            <nodeInfo :node="propNode2"></nodeInfo>
        </div>
        <div>
            <Metrics></Metrics>
        </div>
    </div>
    <span id="sim3" class="sim-label" @click="handleLabel('graph3')" v-if="showLabel3">Simulation 3</span>
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
        <div class="control-panel">
            <button @click="graph3?.fitToContents()" ref="myBtn">Fit</button>
            <button @click="graph3?.zoomIn()">Zoom In</button>
            <button @click="graph3?.zoomOut()">Zoom Out</button>
            <button @click="getGraph()">Get</button>
            <button @click="start(2)">Start/Continue</button>
            <button @click="manualStep(2, 'forward')">Step</button>
            <button @click="manualStep(2, 'back')">Step Back</button>
            <button @click="stop(2)">Stop</button>
        </div>
        <!-- <p class="message"> {{ msg }} </p> -->
        <div id="node-info2" class="node-info" v-if="showNodeInfo3">
            <nodeInfo :node="propNode3"></nodeInfo>
        </div>
        <div>
            <Metrics></Metrics>
        </div>
    </div>
    <span id="sim4" class="sim-label" @click="handleLabel('graph4')" v-if="showLabel4">Simulation 4</span>
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
        <div class="control-panel">
            <button @click="graph4?.fitToContents()" ref="myBtn">Fit</button>
            <button @click="graph4?.zoomIn()">Zoom In</button>
            <button @click="graph4?.zoomOut()">Zoom Out</button>
            <button @click="getGraph()">Get</button>
            <button @click="start(3, )">Start/Continue</button>
            <button @click="manualStep(3, 'forward')">Step</button>
            <button @click="manualStep(3, 'back')">Step Back</button>
            <button @click="stop(3)">Stop</button>
        </div>
        <!-- <p class="message"> {{ msg }} </p> -->
        <div id="node-info2" class="node-info" v-if="showNodeInfo4">
            <nodeInfo :node="propNode4"></nodeInfo>
        </div>
        <div>
            <Metrics></Metrics>
        </div>
    </div>
    <span id="sim5" class="sim-label" @click="handleLabel('graph5')" v-if="showLabel5">Simulation 5</span>
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
        <div class="control-panel">
            <button @click="graph5?.fitToContents()" ref="myBtn">Fit</button>
            <button @click="graph5?.zoomIn()">Zoom In</button>
            <button @click="graph5?.zoomOut()">Zoom Out</button>
            <button @click="getGraph()">Get</button>
            <button @click="start(4)">Start/Continue</button>
            <button @click="manualStep(4, 'forward')">Step</button>
            <button @click="manualStep(4, 'back')">Step Back</button>
            <button @click="stop(4, )">Stop</button>
        </div>
        <!-- <p class="message"> {{ msg }} </p> -->
        <div id="node-info2" class="node-info" v-if="showNodeInfo5">
            <nodeInfo :node="propNode5"></nodeInfo>
        </div>
        <div>
            <Metrics class="metricBtn"></Metrics>
        </div>
    </div>
    <button class="addGraph" @click="addGraph">Add Graph</button>
  </template>

<style>
    .graph-container {
        position:relative;
    }

    .graph {
        width: 100%;
        height: 40em;
        border: 1px solid #ccc;
    }
    .control-panel {
        gap: 10px;
        padding: 10px;
    }
    .message {
        margin:0;
        width: 20%;
        height: 20%;
    }

    .hide {
        display: none;
    }

    .active {
        display: block;
    }

    .node-info {
        position: absolute;
        top: 1em;
        right: 1em;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(206, 206, 206, 0.5);
        border: 1px solid black;
        width: 20em;
        z-index: 1;
    }

    .node-info p {
        margin: 0.5em 0 0.5em 1em;
        padding: 0;
        text-align: left;
        font-size: 0.6em;
        color: black;
    }

    .sim-label {
        display: block;
        background-color: lightblue;
        padding: 1em;
        border: 1px solid black;
        margin-bottom: 1em;
    }
</style>


