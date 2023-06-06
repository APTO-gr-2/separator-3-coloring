def find_two_sides(vertex_list, cycle):
    visited_vertex = dict()
    for v in vertex_list:
        visited_vertex[v] = 0    
    sideA = []
    for v in vertex_list:
        if not v in cycle:
            find_side_rekr(v, sideA, cycle, visited_vertex)
            break
    sideB = []
    for v in vertex_list:
        if not v in cycle and not v in sideA:
            sideB.append(v)
    return sideA, sideB


def find_side_rekr(v, side, cycle, visted_vertex):
    side.append(v)
    visted_vertex[v] = 1
    for u in v.out_neighbors():
        if not u in cycle and visted_vertex[u] == 0:
            find_side_rekr(u, side, cycle, visted_vertex)
