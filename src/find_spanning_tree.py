def find_spanning_tree_rekr(graph, v, visted_vertex):
    spanning_edges = []
    visted_vertex[v] = 1 
    for u in v.out_neighbors():
        if(visted_vertex[u] == 0):
            spanning_edges.extend(graph.edge(v, u, all_edges=True))
            spanning_edges.extend(find_spanning_tree_rekr(graph,u, visted_vertex))
    return spanning_edges
