<script lang="ts">
    import axios from "axios";
    import { reactive, ref } from "vue"
    import * as vNG from "v-network-graph"
    import { Nodes, Edges, Layouts } from "v-network-graph"
    import data from "./data"

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

    var os_type = ''
    var os_version = ''
    var host_ip = ''
    var host_id = ''
    var p_u_compromise = ''
    var total_users = ''
    var uuid = ''
    var total_services = ''
    var total_nodes = ''
    var compromised = ''
    var compromised_services = ''


    var storedGraph = {}
    var number_of_graphs = 0;
    var graphIndex = 0;
    var startSim = false;
    var msg = "Simulation not started"
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
                    graphIndex = 0;
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
                            graphIndex++
                            
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
                    this.graphIndex = -1
                    clearInterval(intervalID)
                    return
                }
                startSim = false
                this.step()
                graphIndex++
                // this.msg = "Stopped"
            },

            step() {
                if (graphIndex == number_of_graphs) {
                    this.msg = "Simulation finished"
                    startSim = false
                    this.graphIndex = -1
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
        },
        data() {
            return {
                msg,
                os_type,
                os_version,
                host_ip,
                host_id,
                p_u_compromise,
                total_users,
                uuid,
                total_services,
                total_nodes,
                compromised,
                compromised_services,
                graph,
                nodes,
                edges,
                layouts,
                selectedNodes,
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
                nodes,
                edges,
                layouts,
            }
        },
        watch: {
            selectedNodes(newVal, oldVal) {
                if (newVal[0]) {
                    console.log(nodes[newVal[0]].host)
                    if (nodes[newVal[0]].host) {
                        this.os_type = nodes[newVal[0]].host.os_type
                        this.os_version = nodes[newVal[0]].host.os_version
                        this.host_ip = nodes[newVal[0]].host.host_ip
                        this.host_id = nodes[newVal[0]].host.host_id
                        this.p_u_compromise = nodes[newVal[0]].host.p_u_compromise
                        this.total_users = nodes[newVal[0]].host.total_users
                        this.uuid = nodes[newVal[0]].host.uuid
                        this.total_services = nodes[newVal[0]].host.total_services
                        this.total_nodes = nodes[newVal[0]].host.total_nodes
                        this.compromised = nodes[newVal[0]].host.compromised
                        console.log(nodes[newVal[0]].host.compromised_services)
                        var compromised_services = ''
                        for (var i = 0; i < nodes[newVal[0]].host.compromised_services.length; i++) {
                            compromised_services += `${nodes[newVal[0]].host.compromised_services[i]}`
                            if (i != nodes[newVal[0]].host.compromised_services.length - 1) {
                                compromised_services += ', '
                            }
                        }
                        this.compromised_services = compromised_services
                    }
                }
                else {
                    this.os_type = ''
                    this.os_version = ''
                    this.host_ip = ''
                    this.host_id = ''
                    this.p_u_compromise = ''
                    this.total_users = ''
                    this.uuid = ''
                    this.total_services = ''
                    this.total_nodes = ''
                    this.compromised = ''
                    this.compromised_services = ''
                }
            }
        },
    }
</script>

<template>
    <v-network-graph id="v-graph"
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
        <button @click="start()">Start</button>
        <button @click="manualStep()">Step</button>
        <button @click="stop()">Stop</button>
    </div>
    <p class="message"> {{ msg }} </p>
    <div class="node-info">
        <p>os type: {{ os_type }}</p>
        <p>os version: {{ os_version }}</p>
        <p>host ip: {{ host_ip }}</p>
        <p>host id: {{ host_id }}</p>
        <p>p_u_compromise: {{ p_u_compromise }}</p>
        <p>total users: {{ total_users }}</p>
        <p>uuid: {{ uuid }}</p>
        <p>total services: {{ total_services }}</p>
        <p>total nodes: {{ total_nodes }}</p>
        <p>compromised: {{ compromised }}</p>
        <p>compromised services: {{ compromised_services }}</p>
    </div>
  </template>

<style>
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
</style>


