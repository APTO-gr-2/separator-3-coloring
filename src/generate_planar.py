import itertools
import random
from graph_tool.all import *


def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)


# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
# Generate a random planar graph with n vertices


def generate_planar_graph(n, m):
    g = Graph(directed=False)
    pos = g.new_vertex_property("vector<double>")
    for i in range(n):
        pos[g.add_vertex()] = [random.uniform(0, 1), random.uniform(0, 1)]

    comb = itertools.combinations(range(n), 2)
    d = list(comb)
    random.shuffle(d)

    c = 0
    for i, j in d:
        if c == m:
            break
        if i == j:
            continue
        for e in g.get_edges():
            if intersect(
                    Point(pos[e[0]][0], pos[e[0]][1]),
                    Point(pos[e[1]][0], pos[e[1]][1]),
                    Point(pos[i][0], pos[i][1]),
                    Point(pos[j][0], pos[j][1])
            ):
                break
        else:
            g.add_edge(i, j)
            if not is_planar(g):
                g.remove_edge(g.edge(i, j))
            else:
                c += 1
    return g, pos
