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

    export default {
        name: 'Network',
        components: {
            vNG,
        },
        methods: {
            getGraph() {
                axios.get("/network/graph").then((res) => {
                    //return length of the data
                    console.log("tests")
                    console.log(res.data)
                    var number_of_graphs = Object.keys(res.data).length
                    // for (var i = 0; i < number_of_graphs; i++) {
                    // console.log(i)
                    var graph = res.data[0]
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
                    // };
                });
            },
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
                        noAutoRestartSimulation: true,
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
    />
    <div class="control-panel">
        <button @click="graph?.fitToContents()">Fit</button>
        <button @click="graph?.zoomIn()">Zoom In</button>
        <button @click="graph?.zoomOut()">Zoom Out</button>
        <button @click="getGraph()">Update</button>
    </div>
  </template>

<style>
    .graph {
      width: 100%;
      height: 100%;
    }
    .control-panel {
      gap: 10px;
      padding: 10px;
    }
</style>
```


