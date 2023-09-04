<!-- Ignore the error message, it works fine. -->

<script setup lang="ts">
  import axios from "axios";
  import { reactive, ref } from "vue"
  import * as vNG from "v-network-graph"
  import { Nodes, Edges } from "v-network-graph"
  import data from "./data"

  // dagre: Directed graph layout for JavaScript
  // https://github.com/dagrejs/dagre
  //@ts-ignore
  import dagre from "dagre/dist/dagre.min.js"

  const nodeSize = 40

  const configs = vNG.defineConfigs({
    view: {
      autoPanAndZoomOnLoad: "fit-content",
      onBeforeInitialDisplay: () => layout(),
      panEnabled: false,
      zoomEnabled: false,
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
      margin: 4,
      marker: {
        target: {
          type: "arrow",
          width: 4,
          height: 4,
        },
      },
    },
  })

  const graph = ref<vNG.VNetworkGraphInstance>()
  const nodes: Nodes = reactive({ ...data.nodes })
  const edges: Edges = reactive({ ...data.edges })
  const nextNodeIndex = ref(Object.keys(nodes).length + 1)
  const nextEdgeIndex = ref(Object.keys(edges).length + 1)

  function layout() {
    if (Object.keys(nodes).length <= 1 || Object.keys(edges).length == 0) {
      return
    }

    // convert graph
    // ref: https://github.com/dagrejs/dagre/wiki
    const g = new dagre.graphlib.Graph()
    // Set an object for the graph label
    g.setGraph({
      rankdir: "LR",
      nodesep: nodeSize * 2,
      edgesep: nodeSize,
      ranksep: nodeSize * 2,
    })
    // Default to assigning a new object as a label for each new edge.
    g.setDefaultEdgeLabel(() => ({}))

    // Add nodes to the graph. The first argument is the node id. The second is
    // metadata about the node. In this case we're going to add labels to each of
    // our nodes.
    Object.entries(nodes).forEach(([nodeId, node]) => {
      g.setNode(nodeId, { label: node.name, width: nodeSize, height: nodeSize })
    })

    // Add edges to the graph.
    Object.values(edges).forEach(edge => {
      g.setEdge(edge.source, edge.target)
    })

    dagre.layout(g)

    g.nodes().forEach((nodeId: string) => {
      // update node position
      const x = g.node(nodeId).x
      const y = g.node(nodeId).y
      data.layouts.nodes[nodeId] = { x, y }
    })
  }

  function addNode() {
    const nodeId = `node${nextNodeIndex.value}`
    const name = `N${nextNodeIndex.value}`
    nodes[nodeId] = { name }
    nextNodeIndex.value++
    addEdge(`node${nextNodeIndex.value - 2}`, `node${nextNodeIndex.value-1}`)
    layout()
    graph.value?.fitToContents()
  }

  function addEdge(source, target) {
    const edgeId = `edge${nextEdgeIndex.value}`
    edges[edgeId] = { source, target }
    nextEdgeIndex.value++
  } 

  function getGraph() {
    axios.get("/network/graph").then((res) => {
      var number_of_nodes = res.data.nodes.length;
      console.log(number_of_nodes);     
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