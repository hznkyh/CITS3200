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
    const layouts: Layouts = reactive({nodes: {},})

    var storedGraph = {}
    var graphIndex = 0
    var msg = ""

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
                });
                graphIndex = 0
            },

            step() {
                this.msg = "Step"
                var number_of_graphs = Object.keys(storedGraph).length
                console.log(storedGraph)
                var graph = storedGraph[graphIndex]
                var nextNodeIndex = 1
                for (var j = 0; j < graph.nodes.length; j++) {
                    const nodeId = `node${graph.nodes[j].id + 1}`
                    const name = `N${nextNodeIndex}`
                    var color = ``
                    // console.log("node: ", j)
                    // TODO change colour
                    if (graph.nodes[j].host.compromised == true) {
                        color = `red`
                    }
                    else {
                        color = `green`
                    }
                    nodes[nodeId] = { name, color}
                    nextNodeIndex++
                }
                var number_of_edges = graph.links.length;
                var nextEdgeIndex = 1
                for (var z = 0; z < number_of_edges; z++) {
                    const edgeId = `edge${nextEdgeIndex}`
                    const source = `node${graph.links[z].source + 1}`
                    const target = `node${graph.links[z].target + 1}`
                    edges[edgeId] = { source, target }
                    nextEdgeIndex++
                };
                graphIndex++
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
                    layoutHandler: new ForceLayout({
                        positionFixedByDrag: false,
                        positionFixedByClickWithAltKey: true,
                        noAutoRestartSimulation: false,
                        createSimulation: (d3, nodes, edges) => {
                        // d3-force parameters
                        const forceLink = d3.forceLink<ForceNodeDatum, ForceEdgeDatum>(edges).id(d => d.id)
                        return d3
                            .forceSimulation(nodes)
                            .force("edge", forceLink.distance(1000).strength(3.0))
                            .force("charge", d3.forceManyBody().strength(-25000))
                            .force("center", d3.forceCenter().strength(0.05))
                            .force("collide", d3.forceCollide().radius(nodeSize * 1.5))
                            .alphaMin(0.001)
                        }
                    }),
                },
                node: {
                    normal: { 
                        radius: nodeSize / 2,
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
        <button @click="step()">Step</button>
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


