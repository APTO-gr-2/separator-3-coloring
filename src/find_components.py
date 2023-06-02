import time
from cmath import sqrt
from types import NoneType

import graph_tool as gt
import numpy as np
from graph_tool.draw import graph_draw
from matplotlib import pyplot as plt
from numpy import average

def find_components(graph): #Szukanie spójnych składowych
    visited_dict = dict()
    for v in graph.vertices():
        visited_dict[v] = 0
    component_list = []
    for v in graph.vertices():
        component = []
        if(visited_dict[v] == 0):
            find_components_rekr(v,component, visited_dict)
        if(len(component) > 0):
            component_list.append(component)
    
    return component_list
            
            
def find_components_rekr(v,component, visited_dict):
    component.append(v)
    visited_dict[v] = 1
    for u in v.out_neighbors():
        if(visited_dict[u] == 0):
            find_components_rekr(u,component, visited_dict)