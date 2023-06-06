def find_spanning_tree_rekr(graph, v, parent, visted_vertex, vertex_ancestors):
    spanning_edges = []
    visted_vertex[v] = 1 
    vertex_ancestors[v] = vertex_ancestors[parent].copy()
    vertex_ancestors[v].insert(0,v)
    for u in v.out_neighbors():
        if(visted_vertex[u] == 0):
            spanning_edges.append(graph.edge(v, u))
            spanning_edges.extend(find_spanning_tree_rekr(graph, u, v, visted_vertex, vertex_ancestors))
    return spanning_edges
