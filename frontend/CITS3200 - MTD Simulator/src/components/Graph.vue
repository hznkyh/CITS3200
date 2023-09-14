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
    const nodes: Nodes = reactive({ ...data.nodes })
    const edges: Edges = reactive({ ...data.edges })
    const layouts: Layouts = reactive({ ...data.layouts})

    var storedGraph = {}
    var number_of_graphs = 0;
    var graphIndex = 0;
    var msg = "Simulation not started"
    var exposed: string[] = [];
    var old_subnets = {}
    var intervalID

    function findExposed(nodeId: string) {
        for (var key in edges) {
            var edge = edges[key]
            if (edge.source == nodeId) {
                exposed.push(edge.target)
            }
        }
    }

    function getRandomCoordinates() {
        const x = Math.random() * (5000 - (-5000)) + (-5000);
        const y = Math.random() * (3000 - (-3000)) + (-3000);
        return { x, y };
    }   

    function layout() {
        console.log("layout")
        // layout the nodes based on their subnet
        var new_subnets = {}
        for (var key in nodes) {
            var node = nodes[key]
            var subnet = node.subnet
            if (subnet in new_subnets) {
                new_subnets[subnet].push(key)
            } else {
               new_subnets[subnet] = [key]
            }
        }
        if (JSON.stringify(new_subnets) == JSON.stringify(old_subnets)) {
            return
        }

        for (var key in new_subnets) {
            var subnet = new_subnets[key]
            var center = getRandomCoordinates()
            var subnetSize = subnet.length
            var subnetRadius = 300
            var angle = 360 / subnetSize
            var angleIndex = 0
            for (var i = 0; i < subnetSize; i++) {
                var x = center.x + subnetRadius * Math.cos(angleIndex * angle * Math.PI / 180) + (Math.floor(Math.random() * 401) - 200)
                var y = center.y + subnetRadius * Math.sin(angleIndex * angle * Math.PI / 180) + (Math.floor(Math.random() * 401) - 200)
                layouts.nodes[subnet[i]] = { x, y }
                angleIndex++
            }
        }
        old_subnets = new_subnets
    }

    // function layout() {
    //     //test graph width and height
    //     layouts.nodes["node1"] = { x: 7000, y: 4000 }
    //     layouts.nodes["node2"] = { x: -7000, y: -4000 }
    // }

    export default {
        name: 'Network',
        components: {
            vNG,
        },
        methods: {
            getGraph() {
                this.msg = "Getting graph..."
                axios.get("/network/graph").then(async (res) => {
                    storedGraph = res.data
                    this.msg = "Got graph"
                    number_of_graphs = Object.keys(storedGraph).length
                    console.log(storedGraph)
                    graphIndex = 0
                });
            },

            start() {
                if (!this.startSim) {
                    this.startSim = true
                    this.msg = "Start"
                    this.step()
                    intervalID = setInterval(() => {
                        if (this.startSim) {
                            this.msg = "Running"
                            this.step()
                            graphIndex++
                            
                        }
                    }, 1500)
                }
            },

            stop() {
                this.startSim = false
                this.msg = "Stopped"

            },

            manualStep() {
                if (graphIndex == number_of_graphs) {
                    this.msg = "Simulation finished"
                    this.startSim = false
                    this.graphIndex = -1
                    clearInterval(intervalID)
                    return
                }
                this.startSim = false
                this.step()
                graphIndex++
                this.msg = "Stopped"
            },

            step() {
                if (graphIndex == number_of_graphs) {
                    this.msg = "Simulation finished"
                    this.startSim = false
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

                    nodes[nodeId] = { name, color, subnet}
                    nextNodeIndex++
                }
                layout()
            },
        },
        data() {
            return {
                msg,
                graph,
                nodes,
                edges,
                layouts,
            }
        },
        setup() {
            const nodeSize = 40

            const configs = vNG.defineConfigs({
                view: {
                    autoPanAndZoomOnLoad: "fit-content",
                    // onBeforeInitialDisplay: () => layout(),
                    autoPanOnResize: true,
                    scalingObjects: true,
                    minZoomLevel: 0.05,
                    maxZoomLevel: 0.2,
                    panEnabled: true,
                    zoomEnabled: true,
                },
                node: {
                    normal: { 
                        radius: nodeSize,
                        color: node => node.color,
                    },
                    label: { direction: "center", color: "#fff" },

                    draggable: true,

                },
                edge: {
                    normal: {
                        color: "#aaa",
                        width: 3,
                    },
                    type: "straight",
                },
            })
            return {
                nodeSize,
                configs,
                graph,
                nodes,
                edges,
                layouts,
            }
        }
    }
</script>

<template>
    <v-network-graph
      ref="graph"
      class="graph"
      :nodes="nodes"
      :edges="edges"
      :layouts="layouts"
      :configs="configs"
    >
    </v-network-graph>
    <div class="control-panel">
        <button @click="graph?.fitToContents()">Fit</button>
        <button @click="graph?.zoomIn()">Zoom In</button>
        <button @click="graph?.zoomOut()">Zoom Out</button>
        <button @click="getGraph()">Get</button>
        <button @click="start()">Start</button>
        <button @click="manualStep()">Step</button>
        <button @click="stop()">Stop</button>
    </div>
    <p class="message"> {{ msg }} </p>
  </template>

<style>
    .graph {
      width: 100%;
      height: 100%;
      border: 1px solid #ccc;
    }
    .control-panel {
      gap: 10px;
      padding: 10px;
    }
    .message {
        margin:0;
    }
</style>
```


