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
        
        console.log("generateCoordinates")
        while (coordinates.length < numCoordinates) {
            const x = Math.random() * (600 - (-600)) + (-600); // Adjust the range as needed
            const y = Math.random() * (350 - (-350)) + (-350); // Adjust the range as needed

            console.log("one iteration")
            // Check if the new coordinates satisfy the minimum distance requirement
            const valid = coordinates.every(([x1, y1]) => {
                return Math.abs(x - x1) >= minDistance && Math.abs(y - y1) >= minDistance;
            });
            if (valid) {
            coordinates.push([x, y]);
            }
        }

        return coordinates;
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

        console.log(new_subnets)

        var coordinates = generateCoordinates(Object.keys(new_subnets).length, 100)

        console.log(coordinates)
        for (var key in new_subnets) {
            var subnet = new_subnets[key]
            var centerx = coordinates[key][0]
            var centery = coordinates[key][1]
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
        }
        old_subnets = new_subnets
    }

    function test() {
        this.$refs.myBtn.click()
    }

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
                layout()
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
                // const graphComponent = this.$refs.graph;
                // // Call the fitToContents method of the component
                // graphComponent.fitToContents();
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
            const nodeSize = 16

            const configs = vNG.defineConfigs({
                view: {
                    autoPanAndZoomOnLoad: "center-zero",
                    // onBeforeInitialDisplay: () => layout(),
                    autoPanOnResize: true,
                    scalingObjects: true,
                    minZoomLevel: 0.5,
                    maxZoomLevel: 0.5,
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
                        radius: nodeSize/2,
                        color: node => node.color,
                    },
                    label: { direction: "center", color: "#fff" },

                    draggable: true,

                },
                edge: {
                    normal: {
                        color: "#aaa",
                        width: 2,
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
    <v-network-graph id="v-graph"
      ref="graph"
      class="graph"
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


