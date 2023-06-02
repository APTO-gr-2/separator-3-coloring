import math
from graph_tool.all import *
import numpy as np
from graph_tool.draw import graph_draw
from matplotlib import pyplot as plt
from numpy import average
import queue

from generate_planar import generate_planar_graph
from find_components import find_components
from find_spanning_tree import find_spanning_tree_rekr

def find_separator(graph, component):
    n = len(component)
    #print(n)
    p = component[0]
    levels = find_levels(component, p)
    r = len(levels)
    k = 0
    l1 = 0
    for level in levels:
        k += len(level)
        if(k >= n/2):
            break
        l1+=1
    l0 = 0
    #print(k)
    for level in levels:
        if(len(level) + 2*(l1 - l0) <= 2*math.sqrt(k)):
            break
        l0+=1
        
    l2 = l1 + 1
    for level in levels[l1 + 1 : -1]:
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
    
    #print(l0,l1,l2)
    #print(Z0, Z1 , Z2)
    separator = []
    if(len(Z0) < n*2.0/3 and len(Z1) < n*2.0/3 and len(Z2) < n*2.0/3):
        separator.extend(levels[l0])
        if(l2 < r):
            separator.extend(levels[l2])
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
            if(len(graph.edge(u, v, all_edges=True)) > 0):
                g_prim.add_edge(g_prim_list[i], g_prim_list[j])
            j +=1
        i+=1
        
    i = 1   
    for v in Z1:
        for u in levels[l0]:
            if(len(graph.edge(u, v, all_edges=True)) > 0):
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
                if(len(g_prim.edge(u, neighbors_list[i], all_edges=True)) == 0):
                    edge = g_prim.add_edge(u, neighbors_list[i])
                    new_edges.append(edge)
            else:
                if(len(g_prim.edge(u, neighbors_list[0], all_edges=True)) == 0):
                    edge = g_prim.add_edge(u, neighbors_list[0])
                    new_edges.append(edge)
            
            i += 1
    visited_vertex = dict()
    for v in g_prim.vertices():
        visited_vertex[v] = 0
    spanning_tree_edges = find_spanning_tree_rekr(g_prim, g_prim_list[0], visited_vertex)
    

    


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
        l += 1
    return levels

    
if __name__ == "__main__":
    (graph,pos) = generate_planar_graph(10, 20)
    #find_separator(graph)
    components_list = find_components(graph)
    for c in components_list:
        separator = find_separator(graph, c)
        print(separator)
    graph_draw(graph, pos)
    

