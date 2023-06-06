import math
from graph_tool.all import *
import numpy as np
from graph_tool.draw import graph_draw
from matplotlib import pyplot as plt
from numpy import average

from generate_planar import generate_planar_graph
from find_components import find_components
from find_spanning_tree import find_spanning_tree_rekr
from find_cycle import find_cycle
from find_two_sides import find_two_sides 

def find_separator(graph, component, isFullAlgoritm):
    n = len(component)
    p = component[0]
    #coloring[p] = 100
    levels = find_levels(component, p)
    r = len(levels)
    k = 0
    l1 = 0
    for level in levels:
        k += len(level)
        if(k >= n/2):
            break
        l1+=1
    
    #for v in levels[l1]:
    #    coloring[v] = 1   
    #print(l1) 
        
    l0 = 0
    for level in levels:
        if(len(level) + 2*(l1 - l0) <= 2*math.sqrt(k)):
            break
        l0+=1
          
        
    l2 = l1 + 1
    for level in levels[l1 + 1 : r]:
        if(len(level) + 2*(l2 - l1 -1) <= 2*math.sqrt(n - k)):
            break
        l2+=1
    
    Z0 = []
    Z1 = []
    Z2 = []
    i = 0
    for level in levels:
        if(i < l0):
            Z0.extend(level)
        elif(i >l0 & i<l2):
            Z1.extend(level)
        elif(i>l2):
            Z2.extend(level)
        i+=1
    

    separator = []
    separator.extend(levels[l0])
    if(l2 < r):
        separator.extend(levels[l2])
    if(len(Z0) < n*2.0/3 and len(Z1) < n*2.0/3 and len(Z2) < n*2.0/3):
        return separator
    
    if(not isFullAlgoritm):
        return separator
    
    g_prim = Graph(directed=False)
    g_prim_list = []
    v0 = g_prim.add_vertex()
    g_prim_list.append(v0)
    v_list = g_prim.add_vertex(len(Z1))
    g_prim_list.extend(v_list)
        
    i = 1
    for v in Z1:
        j = 1
        for u in Z1:
            if graph.edge(u, v) != None:
                g_prim.add_edge(g_prim_list[i], g_prim_list[j])
            j +=1
        i+=1
        
    i = 1   
    for v in Z1:
        for u in levels[l0]:
            if graph.edge(u, v) != None:
                g_prim.add_edge(g_prim_list[i], g_prim_list[0]) 
        i+=1

    new_edges = []
    
    for v in g_prim_list: #Tu jest niby trinagulacja, ale chyba jest źle coś
        i = 1
        neighbors_list = []
        for u in  v.out_neighbors():
            neighbors_list.append(u)
        for u in neighbors_list:
            if(i < len(neighbors_list)):
                if g_prim.edge(u, neighbors_list[i]) == None:
                    edge = g_prim.add_edge(u, neighbors_list[i])
                    new_edges.append(edge)
            else:
                if g_prim.edge(u, neighbors_list[0]) == None:
                    edge = g_prim.add_edge(u, neighbors_list[0])
                    new_edges.append(edge)
            
            i += 1
    visited_vertex = dict()
    vertex_ancestors = dict()
    for v in g_prim.vertices():
        visited_vertex[v] = 0    
    vertex_ancestors[g_prim_list[0]] = []
    spanning_tree_edges = find_spanning_tree_rekr(g_prim, g_prim_list[0],  g_prim_list[0], visited_vertex, vertex_ancestors)
    
    
    for e in g_prim.edges():
        if not e in spanning_tree_edges:
            x = e.source()
            z = e.target()
            cycle, cycle_edges = find_cycle(x, z, vertex_ancestors, g_prim)
            break
    
    sideA, sideB = find_two_sides(g_prim_list, cycle)

    if len(sideA) < len(sideB):
        sideA, sideB = sideB, sideA

    y = None
    loop_limit = 1000 
    i = 0
    while len(sideA) < 2.0/3 * n and len(sideB) < 2.0/3 * n:
        if(i > loop_limit): # Zabezpiecznie przed nieskończoną pętlą
            break
        for v in sideA:
            if g_prim.edge(v, x) != None and g_prim.edge(v, z) != None:
                y = v
                break
        if(y == None):
            break
        if g_prim.edge(x, y) in cycle_edges: #4.13 Przypadek 2.1
            cycle_edges.remove(g_prim.edge(x, y))
            if(g_prim.edge(x, z) in cycle_edges): #tu dziwny błąd , bo normalnie to zawsze powino być prawdą
                cycle_edges.remove(g_prim.edge(x, z))
            cycle_edges.add(g_prim.edge(y, z))
            if(x in cycle): #tu dziwny błąd, bo normalnie to zawsze powino być prawdą
                cycle.remove(x)
            sideB.append(x)
            x = y
        elif g_prim.edge(z, y) in cycle: #4.13 Przypadek 2.2
            cycle_edges.remove(g_prim.edge(y, z))
            cycle_edges.remove(g_prim.edge(x, z))
            cycle_edges.add(g_prim.edge(x, y))
            cycle.remove(z)
            sideB.append(z)
            z = y
        elif g_prim.edge(x, y) in spanning_tree_edges or g_prim.edge(z, y) in spanning_tree_edges:
            cycle_edges.remove(g_prim.edge(x, z))
            cycle_edges.add(g_prim.edge(x, y))
            cycle_edges.add(g_prim.edge(y, z))
            cycle.add(y)
            if(y in sideA): #tu dziwny błąd, bo normalnie to zawsze powino być prawdą
                sideA.remove(y)
            if g_prim.edge(x, y) in spanning_tree_edges:
                x = y
            elif g_prim.edge(z, y) in spanning_tree_edges:
                z = y  
        else:
            cycle1, cycle_edges1 = find_cycle(x, y, vertex_ancestors, g_prim)
            sideA1, sideB1 = find_two_sides(g_prim_list, cycle1)
            if len(sideA1) < len(sideB1):
                sideA1, sideB1 = sideB1, sideA1
            diff1 = len(sideA1) - len(sideB1)
            
            cycle2, cycle_edges2 = find_cycle(y, z, vertex_ancestors, g_prim)
            sideA2, sideB2 = find_two_sides(g_prim_list, cycle2)
            if len(sideA2) < len(sideB2):
                sideA2, sideB2 = sideB2, sideA2
            diff2 = len(sideA2) - len(sideB2)
            
            if(diff1 < diff2): #zamiast maksymalizować większą stronę minimalizuję różnice między częściami
                cycle = cycle1
                sideA = sideA1
                sideB = sideB1
                cycle_edges = cycle_edges1
                z = y
            else:
                cycle = cycle2
                sideA = sideA2
                sideB = sideB2 
                cycle_edges = cycle_edges2 
                x = y
        i += 1
                
    for i in (1, len(g_prim_list)-1):
        if g_prim_list[i] in cycle:
            separator.append(Z1[i-1])
    return separator
    

def find_levels(component, p):
    visited_dict = dict()
    for v in component:
        visited_dict[v] = 0
    levels = [[p]]
    visited_dict[p] = 1
    l = 1
    while True :
        level = []
        for v in levels[l-1]:
            for u in v.out_neighbors():
                if(visited_dict[u] == 0):
                    visited_dict[u] = 1
                    level.append(u)
        if(len(level) == 0):
            break
        levels.append(level)
        l = l + 1
    return levels
    
if __name__ == "__main__":
    (graph,pos) = generate_planar_graph(100, 120)
    components_list = find_components(graph)
    color_map = {0:(1,1,1,1),1:(0,0,1,1),100:(0,0,0,1), 200:(1,0,0,1)}
    coloring = graph.new_vertex_property('int')
    final_coloring = graph.new_vertex_property('vector<double>')
    for c in components_list:
        separator = find_separator(graph, c, True)
        print(separator)
        for v in separator:
            coloring[v] = 200
    for v in graph.vertices():
        final_coloring[v] = color_map[coloring[v]]
    graph_draw(graph,vertex_fill_color=final_coloring,pos = pos)
    

