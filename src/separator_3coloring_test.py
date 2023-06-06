import time

from graph_tool import load_graph, GraphView
from graph_tool.draw import graph_draw

from src.separator_3coloring import separator_3coloring
from src.three_coloring import check_coloring, start_three_coloring

if __name__ == "__main__":
    G = load_graph("../graph4.gt.gz")
    n = 30

    start_time = time.time()
    coloring = separator_3coloring(G, n, show_progress=True)
    end_time = time.time()
    print(end_time - start_time)
    check_coloring(G, GraphView(G), coloring)
    graph_draw(G, vertex_fill_color=coloring)  # , pos=G.vp["pos"])

    start_time = time.time()
    coloring = start_three_coloring(G)
    end_time = time.time()
    print(end_time - start_time)
    check_coloring(G, GraphView(G), coloring)
    graph_draw(G, vertex_fill_color=coloring)  # , pos=G.vp["pos"])
