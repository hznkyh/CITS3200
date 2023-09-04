import networkx as nx


class CustomNode:
    def __init__(self, name, attribute):
        self.name = name
        self.attribute = attribute

    def to_dict(self):
        return {"name": self.name, "attribute": self.attribute}

G = nx.Graph()
node1 = CustomNode("Node1", "Attribute1")
node2 = CustomNode("Node2", "Attribute2")
G.add_edge(node1, node2)

def serialize_graph(graph):
    data = nx.node_link_data(graph)
    serialized_nodes = [node.to_dict() for node in graph.nodes()]
    data["nodes"] = serialized_nodes
    return data


def test_serialize_graph():
    G_test = nx.Graph()
    node1 = CustomNode("Node1", "Attribute1")
    node2 = CustomNode("Node2", "Attribute2")
    G_test.add_edge(node1, node2)

    serialized_graph = serialize_graph(G_test)

    assert serialized_graph["nodes"] == [
        {"name": "Node1", "attribute": "Attribute1"},
        {"name": "Node2", "attribute": "Attribute2"}
    ]

    assert serialized_graph["links"] == [
        {"source": 0, "target": 1}
    ]
