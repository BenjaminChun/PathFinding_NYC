from Astar import Astar
from graph import Graph, Node
from ucs_algorithm import UCS, UCSv2, UCSv3
import json
 


def run():
    # Create graph
    graph = Graph()
    # Opening JSON file
    f = open('Dist.json')
    dist_dict = json.load(f)
    # Closing file
    f.close()
    #COSTdict
    f = open('Cost.json')
    cost_dict = json.load(f)
    f.close()
    #Gdict
    f = open('G.json')
    g_dict = json.load(f)
    f.close()
    #CoordDict
    f = open('Coord.json')
    coord_dict = json.load(f)
    f.close()


    #below dictionary are initialised for testing of algorithm
    gDict = {
      'V1':['V2', 'V3'],
      'V2':['V3', 'V1', 'V4', 'V5'],
      'V3':['V2', 'V1', 'V4', 'V5'],
      'V4':['V2', 'V3', 'V5'],
      'V5':['V2', 'V3', 'V4']
    }

    distDict = {
      'V1,V2':9,
      'V1,V3':4,
      'V2,V3':2,
      'V2,V5':3,
      'V3,V5':6,
      'V2,V4':7,
      'V3,V4':1,
      'V4,V5':3,
      'V2,V1':9,
      'V3,V1':4,
      'V3,V2':2,
      'V5,V2':3,
      'V5,V3':6,
      'V4,V2':7,
      'V4,V3':1,
      'V5,V4':3
    }

    costDict = {
      'V1,V2':6,
      'V1,V3':8,
      'V2,V3':8,
      'V2,V5':2,
      'V3,V5':4,
      'V2,V4':1,
      'V3,V4':7,
      'V4,V5':4,
      'V2,V1':6,
      'V3,V1':8,
      'V3,V2':8,
      'V5,V2':2,
      'V5,V3':4,
      'V4,V2':1,
      'V4,V3':7,
      'V5,V4':4
    }
    # Add vertices
    graph.add_node(Node('V1'))
    graph.add_node(Node('V2'))
    graph.add_node(Node('V3'))
    graph.add_node(Node('V4'))
    graph.add_node(Node('V5'))
    
    # Add edges and distance and fuel cost
    graph.add_edge('V1', 'V2', 9)
    graph.add_edge('V1', 'V3', 4)
    graph.add_edge('V2', 'V3', 2)
    graph.add_edge('V2', 'V4', 7)
    graph.add_edge('V2', 'V5', 3)
    graph.add_edge('V3', 'V4', 1)
    graph.add_edge('V3', 'V5', 6)
    graph.add_edge('V4', 'V5', 4)
  
    #initialise some coordinates
    coordDict={
      'V1':[0,0],
      'V2':[4,5],
      'V3':[2,2],
      'V4':[11,5],
      'V5':[7,5]
    }
    #Part 1:
    print('\n---------------------------------------------\n')
    print("Finding solution for Task 1")
    alg0 = UCS(g_dict, dist_dict, '1', '50')
    path, expansionCount = alg0.search()
    print("Printing solution for Task 1")
    print(" -> ".join(path))
    dis=0
    energy=0
    for i in range(len(path)-1):
      dis+=dist_dict[path[i]+','+path[i+1]]
      energy+=cost_dict[path[i]+','+path[i+1]]
    print(f"Shortest distance: {dis}")
    print(f"Total energy cost: {energy}")
    print(f"Total number of nodes expanded: {expansionCount}")

    #Part 2: With Energy Constraint
    print('\n---------------------------------------------\n')
    print("Finding solution for Task 2")
    alg1 = UCSv2(g_dict, dist_dict, cost_dict, '1', '50')
    path, expansionCount = alg1.search()
    # tempList = [] #keeps track of new graphs neighbours
    # tempGDict = {}
    # for node in tempGraph.nodes:
    #   for neighbor in node.neighbors:
    #     tempList.append(neighbor[0].value)
    #   tempGDict[node.value] = tempList
    #   tempList = []
    
    # alg0 = UCSv3(g_dict, dist_dict, '1', '50', cost_dict)
    # node = alg0.search()
    # path = node[3]
    # temptempGDict = alg0.search()

    # alg1 = UCS(temptempGDict, dist_dict, '1','50')
    # path = alg1.search()
    # print(path)
    print("Printing solution for Task 2")
    print(" -> ".join(path))
    dis=0
    energy=0
    for i in range(len(path)-1):
      dis+=dist_dict[path[i]+','+path[i+1]]
      energy+=cost_dict[path[i]+','+path[i+1]]
    print(f"Shortest distance: {dis}")
    print(f"Total energy cost: {energy}")
    print(f"Total number of nodes expanded: {expansionCount}")

    # Part 3 Modified Astar with fuel constraint
    print('\n---------------------------------------------\n')
    print("Finding solution for Task 3")
    alg1 = Astar(g_dict, dist_dict, '1',"50",cost_dict,coord_dict)
    node_tuple,expansionCount = alg1.search()
    dis=node_tuple[0]
    energy=287932-node_tuple[4]
    path=node_tuple[3]
    print("Printing solution for Task 3")
    print(" -> ".join(path))
    print(f"Shortest distance: {dis}")
    print(f"Total energy cost: {energy}")
    print(f"Total number of nodes expanded: {expansionCount}")



if __name__ == '__main__':
  run()
