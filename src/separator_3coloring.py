from graph_tool import GraphView
from graph_tool.draw import graph_draw

from generate_separated_graph import generate_separated_graph
from src.all_three_colorings import all_three_colorings
from src.find_components import find_components
from three_coloring import three_coloring, check_coloring


def separator_3coloring(G, n):

    coloring = G.new_vertex_property("int")
    coloring.a = -1
    
    return sep3col_rec(G, coloring, GraphView(G), n)


def sep3col_rec(G, coloring, view, n):
    if len(view.get_vertices()) < n:
        return three_coloring(G, view, coloring)

    sep_colorings = [all_three_colorings(G, GraphView(g, vfilt=lambda v: side[v] == 1), coloring)]

    for sep_coloring in sep_colorings:
        graph_draw(g, vertex_fill_color=sep_coloring, pos=pos)
        components = find_components(GraphView(view, vfilt=lambda v: side[v] != 1))
        new_coloring = sep_coloring
        for component in components:
            mask = view.new_vertex_property("bool")
            mask.a = False
            for v in component:
                mask[v] = True
            color = three_coloring(G, GraphView(view, vfilt=mask), new_coloring)
            if color is None:
                print("Failed to find full coloring for this separator coloring")
                break
            new_coloring = color
        else:
            graph_draw(G, vertex_fill_color=new_coloring, pos=pos)
            return new_coloring
    return None




if __name__ == "__main__":
    g, sep_index, side, pos = generate_separated_graph(40, 40, 30)
    graph_draw(g, vertex_fill_color=side, pos=pos)

    n = 100
    coloring = separator_3coloring(g, n)
    graph_draw(g, vertex_fill_color=coloring, pos=pos)
    # vertex_color = g.new_vertex_property("int")
    # vertex_color.a = -1
    # coloring = three_coloring(g,  GraphView(g, vfilt=lambda v: side[v] == 0), vertex_color, pos)
    # graph_draw(g, vertex_fill_color=coloring, pos=pos)
    # coloring = three_coloring(g,  GraphView(g, vfilt=lambda v: side[v] == 1), vertex_color, pos)
    # graph_draw(g, vertex_fill_color=coloring, pos=pos)
    # coloring = three_coloring(g,  GraphView(g, vfilt=lambda v: side[v] == 2), vertex_color, pos)
    # graph_draw(g, vertex_fill_color=coloring, pos=pos)

    check_coloring(g, GraphView(g), coloring)

