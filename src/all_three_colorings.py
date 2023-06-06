from graph_tool import GraphView, PropertyMap

from src.find_components import find_components


def __recur_all_three_colorings(graph, view, vertex_color: PropertyMap, v):
    possible_three_colorings = []
    colorings_to_combine = []
    colorings_to_sum = []
    neighbor_colors = set([vertex_color[n] for n in graph.iter_all_neighbors(v)])
    for color in range(3):
        if color in neighbor_colors:
            continue
        temp_coloring: PropertyMap = vertex_color.copy()
        temp_coloring[v] = color
        iterations = 0  # Check if any neighbours were colored
        for u in view.iter_all_neighbors(v):
            if temp_coloring[u] == -1:
                continue
            iterations += 1
            # Get list of possible colorings
            result_colorings = __recur_all_three_colorings(graph, view, temp_coloring, u)
            colorings_to_combine.append(result_colorings)
        if iterations == 0:
            colorings_to_sum.append(temp_coloring)
        else:
            pass
            # TODO: Make combinations of possible_three_colorings_for_color
    # TODO: Sum the combinations by color
    return possible_three_colorings

def __start_all_three_colorings(graph, view: GraphView, old_coloring):
    possible_three_colorings = []
    v = view.vertex(0, use_index=False)
    neighbor_colors = set([old_coloring[n] for n in graph.iter_all_neighbors(v)])
    if len(neighbor_colors) == 3:
        return []
    # For all three possibilities of coloring the first vertex
    for color in range(3):
        if color in neighbor_colors:
            continue
        possible_three_colorings_for_color = []
        temp_coloring = old_coloring.copy()
        temp_coloring[v] = color
        # color the neighbours of the first vertex using the same method
        for u in view.iter_all_neighbors(v):
            if temp_coloring[u] == -1:
                continue
            # Get list of possible colorings
            result_colorings = __recur_all_three_colorings(graph, view, temp_coloring, u)
            possible_three_colorings_for_color.append(result_colorings)
        # TODO: Make combinations of possible_three_colorings_for_color
    # TODO: Sum the combinations by color
    return possible_three_colorings


def all_three_colorings(graph, view, old_coloring):
    all_components_colorings = []  # List of lists of colorings
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
    return all_components_colorings
