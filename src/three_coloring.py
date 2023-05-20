import time
from cmath import sqrt
from types import NoneType

import graph_tool as gt
import numpy as np
from graph_tool.draw import graph_draw
from matplotlib import pyplot as plt
from numpy import average

from generate_planar import generate_planar_graph


def three_color(coloring, v, hierarchy, what_to_color):
    neighbor_colors = set([coloring[n] for n in v.all_neighbors()])
    #print(f"Choosing color for {v}")
    for color in range(3):
        if color in neighbor_colors:
            #print(f"Choosing color for {v}: not {color}")
            continue
        else:
            #print(f"Choosing color for {v}: chosen {color}")
            coloring[v] = color
            #graph_draw(graph, vertex_fill_color=coloring, pos=pos)
            for u in v.all_neighbors():
                if coloring[u] == -1 and hierarchy[u] == what_to_color:
                    #print(f"Going to {u}")
                    result = three_color(coloring, u, hierarchy,  what_to_color)
                    #coloring[v] = -1
                    if not result:
                        return False
            break
    if coloring[v] == -1:
        return False
    return True


def three_coloring(graph, vertex_color, labels, what_to_color, pos):
    """
    Returns a 3-coloring of the given graph, or None if it is not 3-colorable.
    Only vertices that have value 'what_to_color' in 'labels' property are colored
    """

    # Taking care of all components
    for v in graph.vertices():
        if vertex_color[v] == -1 and labels[v] == what_to_color:
            neighbor_colors = set([vertex_color[n] for n in v.all_neighbors()])
            # Check if it's possible to assign any color
            if len(neighbor_colors) == 3:
                return None
            result = True
            # Try assigning all possibilities
            for color in range(3):
                if color in neighbor_colors:
                    continue
                vertex_color[v] = color
                # graph_draw(graph, vertex_fill_color=coloring, pos=pos)
                for u in v.all_neighbors():
                    if labels[u] != what_to_color:
                        continue
                    result = three_color(vertex_color, u, labels, what_to_color) and result
                    if not result:
                        break
                if result:
                    break # return vertex_color
            if not result:
                return None
    graph_draw(graph, vertex_fill_color=vertex_color, vertex_color=labels, pos=pos)
    check_coloring(graph, vertex_color, labels, what_to_color)
    return vertex_color


def check_coloring(graph, coloring, labels, what_to_color):
    if coloring is None:
        return
    for (s, t) in graph.iter_edges():
        if (labels[s] == what_to_color or labels[t] == what_to_color) and coloring[s] == coloring[t]:
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
        coloring = three_coloring(graph, vertex_color, hierarchy, 0)  # 0 is the index of separator
        end_time = time.time()
    check_coloring(graph, coloring)
    graph_draw(graph, vertex_fill_color=coloring, pos=pos)

