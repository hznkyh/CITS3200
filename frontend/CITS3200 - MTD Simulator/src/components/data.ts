import { Nodes, Edges, Layouts } from "v-network-graph"
import { reactive } from "vue"

const nodes: Nodes = {
  node1: { name: "Node 1", subnet: 0},
  node2: { name: "Node 2", subnet: 0 },
  node3: { name: "Node 3", subnet: 1 },
  node4: { name: "Node 4", subnet: 1 },
  node5: { name: "Node 5", subnet: 2 },
  node6: { name: "Node 6", subnet: 2 },
  node7: { name: "Node 7", subnet: 2 },
}

const edges: Edges = {
  edge1: { source: "node1", target: "node2" },
  edge2: { source: "node2", target: "node3" },
  edge3: { source: "node3", target: "node4" },
}

const layouts: Layouts = reactive({
  nodes: {
    node1: { x: 0, y: 0 },
    node2: { x: 0, y: 100 },
    node3: { x: 100, y: 100 },
    node4: { x: 100, y: 0 },
    node5: { x: 200, y: 0 },
    node6: { x: 200, y: 100 },
    node7: { x: 200, y: 200 },

  },
})

export default {
  nodes,
  edges,
  layouts,
}