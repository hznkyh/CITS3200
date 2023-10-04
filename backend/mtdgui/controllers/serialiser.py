import networkx as nx
from itertools import chain

_attrs = dict(source="source", target="target", name="id", key="key", link="links")
def serialize_graph(G:nx.Graph, attrs=None):
    """Returns data in node-link format that is suitable for JSON serialization
    and use in Javascript documents.

    Parameters
    ----------
    G : NetworkX graph

    attrs : dict
        A dictionary that contains five keys 'source', 'target', 'name',
        'key' and 'link'.  The corresponding values provide the attribute
        names for storing NetworkX-internal graph data.  The values should
        be unique.  Default value::

            dict(source='source', target='target', name='id',
                 key='key', link='links')

        If some user-defined graph data use these attribute names as data keys,
        they may be silently dropped.

    Returns
    -------
    data : dict
       A dictionary with node-link formatted data.

    Raises
    ------
    NetworkXError
        If values in attrs are not unique.

    Examples
    --------

    Notes
    -----
    Graph, node, and link attributes are stored in this format.  Note that
    attribute keys will be converted to strings in order to comply with JSON.
    """
    multigraph = G.is_multigraph()
    # Allow 'attrs' to keep default values.
    if attrs is None:
        attrs = _attrs
    else:
        attrs.update({k: v for (k, v) in _attrs.items() if k not in attrs})
    name = attrs["name"]
    source = attrs["source"]
    target = attrs["target"]
    links = attrs["link"]
    # Allow 'key' to be omitted from attrs if the graph is not a multigraph.
    key = None if not multigraph else attrs["key"]
    if len({source, target, key}) < 3:
        raise nx.NetworkXError("Attribute names are not unique.")
    data = {
        "directed": G.is_directed(),
        "multigraph": multigraph,
        "graph": G.graph,
        "nodes": [serialize_class(G,n,name)  for n in G],
        # "nodes": [dict(chain(G.nodes[n].items(), [(name, n)])) for n in G],
    }
        
    if multigraph:
        data[links] = [
            dict(chain(d.items(), [(source, u), (target, v), (key, k)]))
            for u, v, k, d in G.edges(keys=True, data=True)
        ]
    else:            
        data[links] = [
            dict(chain(d.items(), [(source, u), (target, v)]))
            for u, v, d in G.edges(data=True)
        ]
    return data
    # return data

def serialize_class(G,n,name):
    node = dict(chain(G.nodes[n].items(), [(name, n)]))
    node['host'] = node['host'].toJson()
    return node