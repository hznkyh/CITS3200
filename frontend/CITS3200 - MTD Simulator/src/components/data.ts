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
  node8: { name: "Node 8", subnet: 2 },
  node9: { name: "Node 9", subnet: 2 },
  node10: { name: "Node 10", subnet: 2 },
  node11: { name: "Node 11", subnet: 2 },
  node12: { name: "Node 12", subnet: 2 },

}

const edges: Edges = {
  edge1: { source: "node1", target: "node2" },
  edge2: { source: "node2", target: "node3" },
  edge3: { source: "node3", target: "node4" },
}

const layouts: Layouts = reactive({
  nodes: {
    node1: { x: -800, y: -450 },
    node2: { x: 0, y: 0 },
    node3: { x: 100, y: 100 },
    node4: { x: 100, y: 0 },
    node5: { x: 200, y: 0 },
    node6: { x: 200, y: 100 },
    node7: { x: 200, y: 200 },
    node8: { x: 200, y: 300 },
    node9: { x: 200, y: 400 },
    node10: { x: 200, y: 500 },
    node11: { x: 200, y: 600 },
    node12: { x: 800, y: 450 },

  },
})

export default {
  nodes,
  edges,
  layouts,
}