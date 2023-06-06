from graph_tool import GraphView
from graph_tool.draw import graph_draw

from src.find_components import find_components
from src.find_separator import find_separator
from src.generate_planar import generate_planar_graph
from three_coloring import three_coloring, check_coloring


def separator_3coloring(G, n, show_progress=False):
    coloring = G.new_vertex_property("int")
    coloring.a = -1

    components = find_components(G)
    mask = G.new_vertex_property("bool")
    for component in components:
        mask.a = False
        for v in component:
            mask[v] = True
        coloring = __sep3col_rec(G, component, coloring, GraphView(G, vfilt=mask), n, show_progress)

    return coloring


def __sep3col_rec(G, my_component, coloring, view, n, show_progress, pos=None):
    if len(view.get_vertices()) < n:
        return three_coloring(G, view, coloring)

    separator = find_separator(G, my_component, True)
    separator_mask = G.new_vertex_property("bool")
    separator_mask.a = False
    for v in separator:
        separator_mask[v] = True
    if show_progress:
        print("Current separator")
        graph_draw(G, vertex_fill_color=separator_mask, pos=pos)  # Draw separator
    # sep_colorings = all_three_colorings(G, GraphView(g, vfilt=lambda v: side[v] == 1), coloring)
    sep_colorings = [three_coloring(G, GraphView(view, vfilt=lambda v: separator_mask[v] == True), coloring)]

    for sep_coloring in sep_colorings:
        if sep_coloring is None:
            continue
        if show_progress:
            graph_draw(G, vertex_fill_color=sep_coloring, pos=pos)
        minus_separator = GraphView(view, vfilt=lambda v: separator_mask[v] == False)
        components = find_components(minus_separator)
        new_coloring = sep_coloring
        for component in components:
            mask = view.new_vertex_property("bool")
            mask.a = False
            for v in component:
                mask[v] = True
            if show_progress:
                print("Current component")
                graph_draw(G, vertex_fill_color=mask, pos=pos)
            color = __sep3col_rec(G, component, new_coloring, GraphView(view, vfilt=mask), n, show_progress)
            # color = three_coloring(G, GraphView(view, vfilt=mask), new_coloring)  # Here we color sides
            if color is None:
                if show_progress:
                    print("Failed to find full coloring for this separator coloring")
                    graph_draw(G, vertex_fill_color=new_coloring, pos=pos)
                break
            new_coloring = color
        else:
            if show_progress:
                graph_draw(G, vertex_fill_color=new_coloring, pos=pos)
            return new_coloring
    return None


if __name__ == "__main__":
    # g, sep_index, side, pos = generate_separated_graph(40, 40, 30)

    G, pos = generate_planar_graph(800, 820)
    graph_draw(G, pos=pos)

    n = 100
    coloring = separator_3coloring(G, n)
    graph_draw(G, vertex_fill_color=coloring, pos=pos)

    check_coloring(G, GraphView(G), coloring)
    if coloring is not None:
        G.vp["pos"] = pos
        G.save("graph7.gt.gz")
    print("Done")
