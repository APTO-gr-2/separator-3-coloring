import time
from cmath import sqrt

import graph_tool as gt
import numpy as np
from graph_tool.draw import graph_draw
from matplotlib import pyplot as plt
from numpy import average

from generate_planar import generate_planar_graph


def three_color(graph, view, coloring, v):
    neighbor_colors = set([coloring[n] for n in graph.iter_all_neighbors(v)])
    #print(f"Choosing color for {v}")
    for color in range(3):
        if color in neighbor_colors:
            #print(f"Choosing color for {v}: not {color}")
            continue
        else:
            #print(f"Choosing color for {v}: chosen {color}")
            coloring[v] = color
            #graph_draw(graph, vertex_fill_color=coloring, pos=pos)
            for u in view.iter_all_neighbors(v):
                if coloring[u] == -1:
                    #print(f"Going to {u}")
                    result = three_color(graph, view, coloring, u)
                    #coloring[v] = -1
                    if not result:
                        return False
            break
    if coloring[v] == -1:
        return False
    return True


def three_coloring(graph, view, old_coloring):
    """
    Returns a 3-coloring of the given graph, or None if it is not 3-colorable.
    Only the view is colored.
    """
    if old_coloring is None:
        return None
    vertex_color = old_coloring.copy()
    # Taking care of all components
    for v in view.iter_vertices():
        if vertex_color[v] == -1:
            neighbor_colors = set([vertex_color[n] for n in graph.iter_all_neighbors(v)])
            neighbor_colors.add(-1)
            # Check if it's possible to assign any color
            if len(neighbor_colors) == 4:
                return None
            result = True
            # Try assigning all possibilities
            for color in range(3):
                if color in neighbor_colors:
                    continue
                vertex_color[v] = color
                # graph_draw(graph, vertex_fill_color=coloring, pos=pos)
                for u in view.iter_all_neighbors(v): # TODO: What if one of them gets colored in previous step?
                    result = three_color(graph, view, vertex_color, u) and result
                    if not result:
                        break
                if result:
                    break # return vertex_color
            if not result:
                return None
    # graph_draw(graph, vertex_fill_color=vertex_color, vertex_color=labels, pos=pos)
    check_coloring(graph, view, vertex_color)
    return vertex_color


def check_coloring(graph, view: gt.GraphView, coloring):
    if coloring is None:
        return
    for v in view.iter_vertices():
        for (s, t) in graph.iter_all_edges(v):
            if coloring[s] == coloring[t]:
                raise Exception('Wrong coloring!')


def time_test():
    data = [(x, sqrt(x)) for x in range(5, 100)]
    time_avg = []

    try:
        for i, case in enumerate(data):
            times = []
            for j in range(100):
                coloring = None
                while coloring is None:
                    graph, pos = generate_planar_graph(case[0], case[1])
                    start_time = time.time()
                    coloring = three_coloring(graph)
                    end_time = time.time()
                check_coloring(graph, coloring)
                times.append(end_time - start_time)
            time_avg.append(average(times))
            print(f"{case[0]}: {time_avg[i]:.4}")
    except KeyboardInterrupt as e:
        print(e)

    xpoints = np.array([case[0] for case in data[:len(time_avg)]])
    ypoints = np.array(time_avg)

    plt.plot(xpoints, ypoints, 'o')
    plt.show()

    graph_draw(graph, vertex_fill_color=coloring, pos=pos)


def start_three_coloring(G):
    vertex_color = G.new_vertex_property("int")
    vertex_color.a = -1
    return three_coloring(G, gt.GraphView(G), vertex_color)


if __name__ == "__main__":
    #time_test()
    coloring = None
    while coloring is None:
        graph, pos = generate_planar_graph(30, 150)
        start_time = time.time()
        vertex_color = graph.new_vertex_property("int")
        vertex_color.a = -1
        hierarchy = graph.new_vertex_property("int")
        hierarchy.a = 0
        coloring = three_coloring(graph, vertex_color, hierarchy)  # 0 is the index of separator
        end_time = time.time()
    check_coloring(graph, coloring)
    graph_draw(graph, vertex_fill_color=coloring, pos=pos)

