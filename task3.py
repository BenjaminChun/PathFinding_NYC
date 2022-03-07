from graph import *
from astar_algorithm import *
import math
import json


f = open('G(1).json')
g_dict = json.load(f)
f.close()
#print(g_dict)

f = open('Dist(1).json')
dist_dict = json.load(f)
f.close()
# print(dist_dict['1,2'])

graph = Graph()
for key in g_dict:
    graph.add_node(Node(key))
for key in dist_dict:
    ls=key.split(',')
    # print(type(ls[0]))
    # print(ls[0],ls[1])
    graph.add_edge(ls[0],ls[1],dist_dict[key])
    print(key)
