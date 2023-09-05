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
                    console.log (res.data);
                    var nextNodeIndex = 1
                    for (var i = 0; i < res.data.nodes.length; i++) {
                        const nodeId = `node${res.data.nodes[i].id + 1}`
                        const name = `N${nextNodeIndex}`
                        console.log(nodes)
                        var color = ``
                        // TODO change colour
                        if (res.data.nodes[i].host.compromised != true) {
                            color = `red`
                        }
                        nodes[nodeId] = { name, color}
                        nextNodeIndex++
                    }
                    var number_of_edges = res.data.links.length;
                    var nextEdgeIndex = 1
                    for (var i = 0; i < number_of_edges; i++) {
                        const edgeId = `edge${nextEdgeIndex}`
                        const source = `node${res.data.links[i].source + 1}`
                        const target = `node${res.data.links[i].target + 1}`
                        edges[edgeId] = { source, target }
                        nextEdgeIndex++
                    };
                });
                console.log(graph)
            },
        },
        setup() {
            const nodeSize = 25

            const configs = vNG.defineConfigs({
                view: {
                    autoPanAndZoomOnLoad: "fit-content",
                    // onBeforeInitialDisplay: () => layout(),
                    panEnabled: false,
                    zoomEnabled: false,
                    minZoomLevel: 0.1,
                    maxZoomLevel: 0.1,
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
  </template>
