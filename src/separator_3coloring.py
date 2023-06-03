from graph_tool import GraphView
from graph_tool.draw import graph_draw

from generate_separated_graph import generate_separated_graph
from three_coloring import three_coloring, check_coloring

def separator_3coloring(G, n):

    coloring = G.new_vertex_property("int")
    coloring.a = -1
    
    return sep3col_rec(G, coloring, GraphView(G), n)

def sep3col_rec(G, coloring, view,n):
    pass
   # if len(view.get_vertices()) < n:
       # return three_coloring(n,n,n,n,n)

if __name__ == "__main__":
    g, sep_index, side, pos = generate_separated_graph(10, 10, 10)
    graph_draw(g, vertex_fill_color=side, pos=pos)

    n = 100
    #coloring = separator_3coloring(g, n)

    vertex_color = g.new_vertex_property("int")
    vertex_color.a = -1

    coloring = three_coloring(g,  GraphView(g, vfilt=lambda v: side[v] == 0), vertex_color, pos)
    graph_draw(g, vertex_fill_color=coloring, pos=pos)
    coloring = three_coloring(g,  GraphView(g, vfilt=lambda v: side[v] == 1), vertex_color, pos)
    graph_draw(g, vertex_fill_color=coloring, pos=pos)
    coloring = three_coloring(g,  GraphView(g, vfilt=lambda v: side[v] == 2), vertex_color, pos)
    graph_draw(g, vertex_fill_color=coloring, pos=pos)

    check_coloring(g, GraphView(g), coloring)

