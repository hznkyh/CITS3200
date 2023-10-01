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

    import {
        ForceLayout,
        ForceNodeDatum,
        ForceEdgeDatum,
    } from "v-network-graph/lib/force-layout"

    const graph = ref<vNG.VNetworkGraphInstance>()
    var nodes: Nodes = reactive({ ...data.nodes })
    var edges: Edges = reactive({ ...data.edges })
    var layouts: Layouts = reactive({ ...data.layouts})
    const selectedNodes = ref<string[]>([])

    const graph2 = ref<vNG.VNetworkGraphInstance>()
    var nodes2: Nodes = reactive({ ...data2.nodes })
    var edges2: Edges = reactive({ ...data2.edges })
    const selectedNodes2 = ref<string[]>([])

    const graph3 = ref<vNG.VNetworkGraphInstance>()
    var nodes3: Nodes = reactive({ ...data3.nodes })
    var edges3: Edges = reactive({ ...data3.edges })
    const selectedNodes3 = ref<string[]>([])

    const graph4 = ref<vNG.VNetworkGraphInstance>()
    var nodes4: Nodes = reactive({ ...data4.nodes })
    var edges4: Edges = reactive({ ...data4.edges })
    const selectedNodes4 = ref<string[]>([])

    const graph5 = ref<vNG.VNetworkGraphInstance>()
    var nodes5: Nodes = reactive({ ...data5.nodes })
    var edges5: Edges = reactive({ ...data5.edges })
    const selectedNodes5 = ref<string[]>([])

    var number_of_sims = 1;

    var storedGraph = {}
    var number_of_graphs = 0;
    var graphIndex = -1;
    var startSim = false;
    // var msg = "Simulation not started"
    var exposed: string[] = [];
    var old_subnets = {}
    var intervalID

    function clearData() {
        // Clear the nodes object
        for (const key in nodes) {
            if (Object.hasOwnProperty.call(nodes, key)) {
            delete nodes[key];
            }
        }

        // Clear the edges object
        for (const key in edges) {
            if (Object.hasOwnProperty.call(edges, key)) {
            delete edges[key];
            }
        }

        // Clear the layouts object
        for (const key in layouts["nodes"]) {
            if (Object.hasOwnProperty.call(layouts["nodes"], key)) {
            delete layouts["nodes"][key];
            }
        }
    }

    function findExposed(nodeId: string) {
        for (var key in edges) {
            var edge = edges[key]
            if (edge.source == nodeId) {
                exposed.push(edge.target)
            }
        }
    }

    function getRandomCoordinates(centerx, centery) {
        var offset = Math.random() * (350 - (-350)) + (-350);
        var x = centerx + offset
        var y = centery + offset

        var rangex = [-700, 700]
        var rangey = [-350, 350]

        x = Math.min(Math.max(x, rangex[0]), rangex[1])
        y = Math.min(Math.max(y, rangey[0]), rangey[1])
        return { x, y };
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

    function layout() {
        // layout the nodes based on their subnet
        var new_subnets = {}
        for (var key in nodes) {
            var node = nodes[key]
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
                layouts.nodes[subnet[i]] = { x, y }
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
        },
        methods: {
            async getGraph() {
                startSim = false;
                try {
                    clearData();
                    clearInterval(intervalID);
                    this.msg = "Getting graph...";
                    const response = await axios.get("/network/graph");
                    storedGraph = response.data;
                    number_of_graphs = Object.keys(storedGraph).length;
                    graphIndex = -1;
                    this.msg = "Got graph";
                } catch (error) {
                }
            },

            start() {
                if (!startSim) {
                    startSim = true
                    this.msg = "Start"
                    intervalID = setInterval(() => {
                        if (startSim) {
                            // this.msg = "Running"
                            this.step()
                        }
                    }, 1500)
                }
            },

            stop() {
                startSim = false
                this.msg = "Stopped"

            },

            manualStep() {
                if (graphIndex == number_of_graphs) {
                    this.msg = "Simulation finished"
                    startSim = false
                    graphIndex = -2
                    clearInterval(intervalID)
                    return
                }
                if (graphIndex == -2) {
                    return
                }
                startSim = false
                this.step()
                // this.msg = "Stopped"
            },

            step() {
                graphIndex++
                if (graphIndex == number_of_graphs) {
                    this.msg = "Simulation finished"
                    startSim = false
                    graphIndex = -2
                    clearInterval(intervalID)
                    return
                }
                exposed = [];
                var graph = storedGraph[graphIndex]

                var number_of_edges = graph.links.length;
                var nextEdgeIndex = 1
                for (var z = 0; z < number_of_edges; z++) {
                    const edgeId = `edge${nextEdgeIndex}`
                    const source = `node${graph.links[z].source + 1}`
                    const target = `node${graph.links[z].target + 1}`
                    edges[edgeId] = { source, target }
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
                        findExposed(nodeId)
                    } else if (exposed.includes(nodeId)) {
                        color = `yellow`
                    }
                    else {
                        color = `green`
                    }
                    var host = node.host

                    nodes[nodeId] = {color, subnet, layer, host}
                    nextNodeIndex++
                }
                console.log(nodes)
                layout()
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

                graph,
                nodes,
                edges,
                layouts,
                selectedNodes,
                showNodeInfo: false,
                showLabel1: true,
                showGraph:false,
                propNode:null,

                graph2,
                nodes2,
                edges2,
                selectedNodes2,
                showNodeInfo2: false,
                showLabel2: false,
                showGraph2: false,
                propNode2:null,

                graph3,
                nodes3,
                edges3,
                selectedNodes3,
                showNodeInfo3: false,
                showLabel3: false,
                showGraph3: false,
                propNode3:null,

                graph4,
                nodes4,
                edges4,
                selectedNodes4,
                showNodeInfo4: false,
                showLabel4: false,
                showGraph4: false,
                propNode4:null,

                graph5,
                nodes5,
                edges5,
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
        :nodes="nodes"
        :edges="edges"
        :layouts="layouts"
        :configs="configs"
        >
        </v-network-graph>
        <div class="control-panel">
            <button @click="graph?.fitToContents()" ref="myBtn">Fit</button>
            <button @click="graph?.zoomIn()">Zoom In</button>
            <button @click="graph?.zoomOut()">Zoom Out</button>
            <button @click="getGraph()">Get</button>
            <button @click="start()">Start/Continue</button>
            <button @click="manualStep()">Step</button>
            <button @click="stop()">Stop</button>
        </div>
        <!-- <p class="message"> {{ msg }} </p> -->
        <div id="node-info" class="node-info" v-if="showNodeInfo" ref="nodeInfo">
            <nodeInfo :node="propNode"></nodeInfo>
        </div>
    </div>

    <span id="sim2" class="sim-label" @click="handleLabel('graph2')" v-if="showLabel2">Simulation 2</span>
    <div id="graph2" class="graph-container" v-if="showGraph2">
        <v-network-graph 
        ref="graph2"
        class="graph"
        v-model:selected-nodes="selectedNodes2"
        :nodes="nodes2"
        :edges="edges2"
        :layouts="layouts"
        :configs="configs"
        >
        </v-network-graph>
        <div class="control-panel">
            <button @click="graph2?.fitToContents()" ref="myBtn">Fit</button>
            <button @click="graph2?.zoomIn()">Zoom In</button>
            <button @click="graph2?.zoomOut()">Zoom Out</button>
            <button @click="getGraph()">Get</button>
            <button @click="start()">Start/Continue</button>
            <button @click="manualStep()">Step</button>
            <button @click="stop()">Stop</button>
        </div>
        <!-- <p class="message"> {{ msg }} </p> -->
        <div id="node-info2" class="node-info" v-if="showNodeInfo2">
            <nodeInfo :node="propNode2"></nodeInfo>
        </div>
    </div>
    <span id="sim3" class="sim-label" @click="handleLabel('graph3')" v-if="showLabel3">Simulation 3</span>
    <div id="graph3" class="graph-container" v-if="showGraph3">
        <v-network-graph 
        ref="graph3"
        class="graph"
        v-model:selected-nodes="selectedNodes3"
        :nodes="nodes3"
        :edges="edges3"
        :layouts="layouts"
        :configs="configs"
        >
        </v-network-graph>
        <div class="control-panel">
            <button @click="graph3?.fitToContents()" ref="myBtn">Fit</button>
            <button @click="graph3?.zoomIn()">Zoom In</button>
            <button @click="graph3?.zoomOut()">Zoom Out</button>
            <button @click="getGraph()">Get</button>
            <button @click="start()">Start/Continue</button>
            <button @click="manualStep()">Step</button>
            <button @click="stop()">Stop</button>
        </div>
        <!-- <p class="message"> {{ msg }} </p> -->
        <div id="node-info2" class="node-info" v-if="showNodeInfo3">
            <nodeInfo :node="propNode3"></nodeInfo>
        </div>
    </div>
    <span id="sim4" class="sim-label" @click="handleLabel('graph4')" v-if="showLabel4">Simulation 4</span>
    <div id="graph4" class="graph-container" v-if="showGraph4">
        <v-network-graph 
        ref="graph4"
        class="graph"
        v-model:selected-nodes="selectedNodes4"
        :nodes="nodes4"
        :edges="edges4"
        :layouts="layouts"
        :configs="configs"
        >
        </v-network-graph>
        <div class="control-panel">
            <button @click="graph4?.fitToContents()" ref="myBtn">Fit</button>
            <button @click="graph4?.zoomIn()">Zoom In</button>
            <button @click="graph4?.zoomOut()">Zoom Out</button>
            <button @click="getGraph()">Get</button>
            <button @click="start()">Start/Continue</button>
            <button @click="manualStep()">Step</button>
            <button @click="stop()">Stop</button>
        </div>
        <!-- <p class="message"> {{ msg }} </p> -->
        <div id="node-info2" class="node-info" v-if="showNodeInfo4">
            <nodeInfo :node="propNode4"></nodeInfo>
        </div>
    </div>
    <span id="sim5" class="sim-label" @click="handleLabel('graph5')" v-if="showLabel5">Simulation 5</span>
    <div id="graph5" class="graph-container" v-if="showGraph5">
        <v-network-graph 
        ref="graph5"
        class="graph"
        v-model:selected-nodes="selectedNodes5"
        :nodes="nodes5"
        :edges="edges5"
        :layouts="layouts"
        :configs="configs"
        >
        </v-network-graph>
        <div class="control-panel">
            <button @click="graph5?.fitToContents()" ref="myBtn">Fit</button>
            <button @click="graph5?.zoomIn()">Zoom In</button>
            <button @click="graph5?.zoomOut()">Zoom Out</button>
            <button @click="getGraph()">Get</button>
            <button @click="start()">Start/Continue</button>
            <button @click="manualStep()">Step</button>
            <button @click="stop()">Stop</button>
        </div>
        <!-- <p class="message"> {{ msg }} </p> -->
        <div id="node-info2" class="node-info" v-if="showNodeInfo5">
            <nodeInfo :node="propNode5"></nodeInfo>
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


