<!-- Ignore the error message, it works fine. -->

<script setup lang="ts">
  import axios from "axios";
  import { reactive, ref } from "vue"
  import * as vNG from "v-network-graph"
  import { Nodes, Edges } from "v-network-graph"
  import data from "./data"

  import {
    ForceLayout,
    ForceNodeDatum,
    ForceEdgeDatum,
  } from "v-network-graph/lib/force-layout"

  const nodeSize = 25

  const configs = vNG.defineConfigs({
    view: {
      autoPanAndZoomOnLoad: "fit-content",
      // onBeforeInitialDisplay: () => layout(),
      panEnabled: false,
      zoomEnabled: false,
      layoutHandler: new ForceLayout({
        positionFixedByDrag: false,
        positionFixedByClickWithAltKey: true,
        createSimulation: (d3, nodes, edges) => {
          // d3-force parameters
          const forceLink = d3.forceLink<ForceNodeDatum, ForceEdgeDatum>(edges).id(d => d.id)
          return d3
            .forceSimulation(nodes)
            .force("edge", forceLink.distance(80).strength(2.0))
            .force("charge", d3.forceManyBody().strength(-10000))
            .force("center", d3.forceCenter().strength(0.05))
            .force('collision', d3.forceCollide().radius(nodeSize))
            .alphaMin(0.001)
        }
      }),
    },
    node: {
      normal: { radius: nodeSize / 2 },
      label: { direction: "center", color: "#fff" },
      draggable: false,
    },
    edge: {
      normal: {
        color: "#aaa",
        width: 3,
      },
      type: "straight",
    },
  })

  const graph = ref<vNG.VNetworkGraphInstance>()
  const nodes: Nodes = reactive({ ...data.nodes })
  const edges: Edges = reactive({ ...data.edges })
  const nextNodeIndex = ref(Object.keys(nodes).length + 1)
  const nextEdgeIndex = ref(Object.keys(edges).length + 1)

  function addNode() {
    const nodeId = `node${nextNodeIndex.value}`
    const name = `N${nextNodeIndex.value}`
    nodes[nodeId] = { name }
    nextNodeIndex.value++
  }

  function addEdge(source, target) {
    const edgeId = `edge${nextEdgeIndex.value}`
    edges[edgeId] = { source, target }
    nextEdgeIndex.value++
  } 

  function getGraph() {
    axios.get("/network/graph").then((res) => {
      console.log (res.data);
      var number_of_nodes = res.data.nodes.length;
      for (var i = 0; i < number_of_nodes; i++) {
        addNode();
      }
      var number_of_edges = res.data.links.length;
      for (var i = 0; i < number_of_edges; i++) {
        addEdge(`node${res.data.links[i].source + 1}`, `node${res.data.links[i].target + 1}`);
      }
    });
  }
</script>

<template>
  <div class="demo-control-panel">
    <div>
      <label>Node:</label>
      <button @click="addNode">add</button>
      <button @click="graph?.fitToContents()">Fit</button>
      <button @click="getGraph">Get Graph</button>
    </div>
  </div>
  <v-network-graph
    ref="graph"
    class="graph"
    :nodes="nodes"
    :edges="edges"
    :layouts="data.layouts"
    :configs="configs"
  />
</template>