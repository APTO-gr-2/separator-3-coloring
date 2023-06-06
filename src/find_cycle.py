def find_cycle(u, v, vertex_ancestors, graph):
    cycle = {u, v}
    cycle_edge = {graph.edge(u, v)}
    last = u
    print(u)
    print(v)
    print(vertex_ancestors[u])
    print(vertex_ancestors[v])
    for k in vertex_ancestors[u]:
        if not k in vertex_ancestors[v]: #Sprawdzić kolejność na liście
            cycle.add(k)
        else:
            last = v
            break
    for k in vertex_ancestors[v]:
        if not k in vertex_ancestors[u]:
            cycle.add(k)
    cycle.add(last)
    return cycle