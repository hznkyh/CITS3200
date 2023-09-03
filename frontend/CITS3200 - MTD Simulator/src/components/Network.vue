<!-- Ignore the error message, it works fine. -->

<script setup lang="ts">
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

function layout() {
  if (Object.keys(data.nodes).length <= 1 || Object.keys(data.edges).length == 0) {
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
  Object.entries(data.nodes).forEach(([nodeId, node]) => {
    g.setNode(nodeId, { label: node.name, width: nodeSize, height: nodeSize })
  })

  // Add edges to the graph.
  Object.values(data.edges).forEach(edge => {
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

const nodes: Nodes = reactive({ ...data.nodes })
const edges: Edges = reactive({ ...data.edges })
const nextNodeIndex = ref(Object.keys(nodes).length + 1)
const nextEdgeIndex = ref(Object.keys(edges).length + 1)

function addNode() {
  const nodeId = `node${nextNodeIndex.value}`
  const name = `N${nextNodeIndex.value}`
  nodes[nodeId] = { name }
  nextNodeIndex.value++
  console.log("add node", nodeId)
}
</script>

<template>
  <div class="demo-control-panel">
    <div>
      <label>Node:</label>
      <button @click="addNode">add</button>
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