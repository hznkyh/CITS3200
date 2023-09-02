import networkx as nx
from fastapi.responses import JSONResponse
from fastapi import APIRouter


router = APIRouter(prefix="/network", tags=["network"],responses={404: {"description":"Not found"}})


class CustomNode:
    def __init__(self, name, attribute):
        self.name = name
        self.attribute = attribute

    def to_dict(self):
        return {"name": self.name, "attribute": self.attribute}

def serialize_graph(graph):
    data = nx.node_link_data(graph)
    serialized_nodes = [node.to_dict() for node in graph.nodes()]
    data["nodes"] = serialized_nodes
    return data

G = nx.Graph()
node1 = CustomNode("Node1", "Attribute1")
node2 = CustomNode("Node2", "Attribute2")
G.add_edge(node1, node2)

@router.get("/")
async def read_items():
    return "Hello World"

@router.get("/graph") 
def get_item_1():
    graph_data = serialize_graph(G)
    return JSONResponse(content=graph_data)
