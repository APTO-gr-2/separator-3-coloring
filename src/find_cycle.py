def find_cycle(u, v, vertex_ancestors, graph):
    cycle = {u, v}
    cycle_edges = {graph.edge(u, v)}
    last = u
    previous = v
    for k in vertex_ancestors[u]:
        if not k in vertex_ancestors[v]: #Sprawdzić kolejność na liście
            cycle.add(k)
            cycle_edges.add(graph.edge(previous, k))
            previous = k
        else:
            last = k
            break
    previous = u
    for k in vertex_ancestors[v]:
        if not k in vertex_ancestors[u]:
            cycle.add(k)
            cycle_edges.add(graph.edge(previous, k))
            previous = k
    cycle.add(last)
    cycle_edges.add(graph.edge(previous, last))
    return cycle, cycle_edges