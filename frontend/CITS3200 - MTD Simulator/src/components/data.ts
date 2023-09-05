import { Nodes, Edges, Layouts } from "v-network-graph"
import { reactive } from "vue"

const nodes: Nodes = {
}

const edges: Edges = {
}

const layouts: Layouts = reactive({
  nodes: {},
})

export default {
  nodes,
  edges,
  layouts,
}