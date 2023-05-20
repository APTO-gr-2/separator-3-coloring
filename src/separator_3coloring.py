from graph_tool.draw import graph_draw

from generate_separated_graph import generate_separated_graph
from three_coloring import three_coloring, check_coloring

if __name__ == "__main__":
    g, sep_index, side, pos = generate_separated_graph(10, 10, 10)
    graph_draw(g, vertex_fill_color=side, pos=pos)

    # Initialize the colors of the vertices to -1
    vertex_color = g.new_vertex_property("int")
    vertex_color.a = -1
    coloring = three_coloring(g, vertex_color, side, 0, pos)
    graph_draw(g, vertex_fill_color=coloring, pos=pos)
    coloring = three_coloring(g, vertex_color, side, 1, pos)
    graph_draw(g, vertex_fill_color=coloring, pos=pos)
    coloring = three_coloring(g, vertex_color, side, 2, pos)
    graph_draw(g, vertex_fill_color=coloring, pos=pos)

    check_coloring(g, coloring, g.new_vertex_property("bool", val=True), True)

