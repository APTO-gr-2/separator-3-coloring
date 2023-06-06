from graph_tool import GraphView, PropertyMap, Graph
from graph_tool.draw import graph_draw

from src.find_components import find_components


def __recur_all_three_colorings(graph, view, vertex_color: PropertyMap, v):
    colorings_to_combine = []
    colorings_to_sum = []
    neighbor_colors = set([vertex_color[n] for n in graph.iter_all_neighbors(v)])
    for color in range(3):
        if color in neighbor_colors:
            continue
        temp_coloring: PropertyMap = vertex_color.copy()
        temp_coloring[v] = color
        graph_draw(graph, vertex_fill_color=temp_coloring, pos=pos)  # TEST
        iterations = 0  # Check if any neighbours were colored
        for neigh_id, u in enumerate(view.iter_all_neighbors(v)):
            if temp_coloring[u] != -1:
                continue
            iterations += 1
            # Get list of possible colorings
            result_colorings = __recur_all_three_colorings(graph, view, temp_coloring, u)
            if len(colorings_to_combine) == neigh_id:  # TODO: how the hell to mash up the combinations into right arrays?
                colorings_to_combine.append([])
            colorings_to_combine[neigh_id].append(result_colorings)  # list of lists of mappings
        if iterations == 0:
            colorings_to_sum.append(temp_coloring)
        else:
            # TODO: All combinations: while combination_iterator < len
            counter = [0] * len(colorings_to_combine)
            combination_iterator = 0
            combined_coloring = temp_coloring.copy()
            for v in view.iter_vertices():
                index = -1
                for i, j in enumerate(counter):
                    if colorings_to_combine[i][j][v] != -1:
                        # if index != -1:
                        #     raise Exception("conflict while creating combinations!")
                        index = i
                if index == -1:
                    raise Exception("Missing coloring for one vertex!")
                color = colorings_to_combine[index][counter[index]][v]
                combined_coloring[v] = color
            colorings_to_sum.append(combined_coloring)
            combination_iterator += 1
    return colorings_to_sum


def __start_all_three_colorings(graph, view: GraphView, old_coloring):
    colorings_to_combine = []
    colorings_to_sum = []
    v = view.vertex(0, use_index=False)
    neighbor_colors = set([old_coloring[n] for n in graph.iter_all_neighbors(v)])
    # For all three possibilities of coloring the first vertex
    for color in range(3):
        if color in neighbor_colors:
            continue
        temp_coloring: PropertyMap = old_coloring.copy()
        temp_coloring[v] = color
        graph_draw(graph, vertex_fill_color=temp_coloring, pos=pos)  # TEST
        iterations = 0  # Check if any neighbours were colored
        for neigh_id, u in enumerate(view.iter_all_neighbors(v)):
            if temp_coloring[u] != -1:
                continue
            iterations += 1
            # Get list of possible colorings
            result_colorings = __recur_all_three_colorings(graph, view, temp_coloring, u)
            if len(colorings_to_combine) == neigh_id:
                colorings_to_combine.append([])
            colorings_to_combine[neigh_id].append(result_colorings)  # list of lists of mappings
        if iterations == 0:
            colorings_to_sum.append(temp_coloring)
        else:
            # TODO: All combinations: while combination_iterator < len
            counter = [0] * len(colorings_to_combine)
            combination_iterator = 0
            combined_coloring = temp_coloring.copy()
            for v in view.iter_vertices():
                index = -1
                for i, j in enumerate(counter):
                    if colorings_to_combine[i][j][v] != -1:
                        # if index != -1:
                        #     raise Exception("conflict while creating combinations!")
                        index = i
                if index == -1:
                    raise Exception("Missing coloring for one vertex!")
                color = colorings_to_combine[index][counter[index]][v]
                combined_coloring[v] = color
            colorings_to_sum.append(combined_coloring)
            combination_iterator += 1
    return colorings_to_sum


def all_three_colorings(graph, view, old_coloring):
    all_components_colorings = []  # List of lists of colorings
    final_colorings = []
    components = find_components(view)
    component_views = []
    for component in components:
        mask = view.new_vertex_property("bool")
        mask.a = False
        for v in component:
            mask[v] = True
        component_views.append(GraphView(view, vfilt=mask))
    for component_view in component_views:
        component_colorings = __start_all_three_colorings(graph, component_view, old_coloring)
        if not component_colorings:
            return []
        all_components_colorings.append(component_colorings)

    # TODO: Here generate for combinations of components colorings
    counter = [0] * len(all_components_colorings)
    combination_iterator = 0
    combined_coloring = old_coloring.copy()
    for v in view.iter_vertices():
        index = -1
        for i, j in enumerate(counter):
            if all_components_colorings[i][j] != -1:
                # if index != -1:
                #    raise Exception("conflict while creating combinations!")
                index = i
        if index == -1:
            raise Exception("Missing coloring for one vertex!")
        color = all_components_colorings[index][counter[index]][v]
        combined_coloring[v] = color
    final_colorings.append(combined_coloring)
    combination_iterator += 1
    #
    return final_colorings


if __name__ == "__main__":
    g = Graph(directed=False)

    # g.add_vertex(4)
    # g.add_edge_list([(0, 1), (1, 2), (2, 3), (3, 0)])
    g.add_vertex(3)
    g.add_edge_list([(0, 1), (1, 2), (2, 0)])

    coloring = g.new_vertex_property("int")
    coloring.a = -1

    pos = g.new_vertex_property("vector<double>")
    pos[0] = [0, 0]
    pos[1] = [0, 1]
    pos[2] = [1, 1]
    #pos[3] = [1, 0]


    graph_draw(g, vertex_fill_color=coloring, pos=pos)
    colorings = all_three_colorings(g, GraphView(g), coloring)
    for col in colorings:
        print("Printing result coloring")
        graph_draw(g, vertex_fill_color=col, pos=pos)