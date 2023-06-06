import itertools
import random

from graph_tool import Graph
from graph_tool.draw import graph_draw


def generate_separated_graph(n1, sep_size, n2):
    g = Graph(directed=False)
    sep_index = g.new_vertex_property("int")
    side = g.new_vertex_property("int")
    pos = g.new_vertex_property("vector<double>")
    v1 = []
    v2 = []
    sep = []
    for i in range(sep_size):
        v = g.add_vertex()
        sep.append(v)
        sep_index[v] = 1
        side[v] = 1
        pos[v] = [0.5, random.uniform(0, 1)]
    for i in range(n1):
        v = g.add_vertex()
        v1.append(v)
        sep_index[v] = 0
        side[v] = 0
        pos[v] = [random.uniform(0, 0.4), random.uniform(0, 1)]
    for i in range(n2):
        v = g.add_vertex()
        v2.append(v)
        sep_index[v] = 0
        side[v] = 2
        pos[v] = [random.uniform(0.6, 1), random.uniform(0, 1)]

    for set in [sep, v1, v2]:
        sep_edges = list(itertools.combinations(set, 2))
        random.shuffle(sep_edges)
        edge_count = random.randint(int(len(sep_edges) ** 0.3), int(len(sep_edges) ** 0.5))
        for i in range(edge_count):
            g.add_edge(sep_edges[i][0], sep_edges[i][1])

    for set in [(sep, v1), (sep, v2)]:
        sep_edges = [(x,y) for x in set[0] for y in set[1]]
        random.shuffle(sep_edges)
        edge_count = random.randint(int(len(set[0]) ** 0.5), len(set[0]))
        for i in range(edge_count):
            g.add_edge(sep_edges[i][0], sep_edges[i][1])

    return g, sep_index, side, pos


if __name__ == "__main__":
    g, sep_index, side, pos = generate_separated_graph(10, 10, 10)
    graph_draw(g, vertex_fill_color=side, pos=pos)
