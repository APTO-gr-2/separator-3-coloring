from random import *
import math

from generate_planar import generate_planar_graph
from find_components import find_components
from find_separator import find_separator

def check_separator(separator, component):
    n = len(component)
    visited_dict = dict()
    for v in component:
        visited_dict[v] = 0

    flag = True
    for v in component:
        separated = []
        if(visited_dict[v] == 0 and not v in separator):
            check_separator_rekr(separator, v, separated, visited_dict)
        if(len(separated) > n*2/3):
            flag = False
    
    if(flag):
        #print("OK")
        return 1
    else:
        #print("Too big separated components")
        return 0


        
            
def check_separator_rekr(separator, v, separated, visited_dict):
    separated.append(v)
    visited_dict[v] = 1
    for u in v.out_neighbors():
        if(visited_dict[u] == 0 and not v in separator):
            check_separator_rekr(separator, u, separated, visited_dict)


if __name__ == "__main__":
    while True:
        n = randint(1, 200)
        m = randint(1, 200)
        (graph,pos) = generate_planar_graph(n, m)
        components_list = find_components(graph)
        positive_answers = 0 
        for c in components_list:
            separator = find_separator(graph, c, True)
            if(len(separator) > 2 * math.sqrt(2) * math.sqrt(len(c))):
                #print("Too big separator")
                {}
            else:
                positive_answers += check_separator(separator, c)
        print(positive_answers,"/",len(components_list))
       
    

