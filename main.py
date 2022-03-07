from graph import Graph, Node
from ucs_algorithm import UCS, UCSv2
import json
 
# Opening JSON file

def run():
    # Create graph
    graph = Graph()
    # Opening JSON file
    # with open('data.json') as json_file:
    #     data = json.load(json_file)
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


    # Execute the algorithm
    alg = UCSv2(graph, distDict, costDict, "V1", "V4")
    tempGraph = alg.search()
    for node in tempGraph.nodes:
      print(node.value)
      for neighbor in node.neighbors:
        print((neighbor[0].value, neighbor[1]))
      print("--------------------")
    
    alg0 = UCSv2(tempGraph, distDict, costDict, "V4", "V1")
    temptempGraph = alg0.search()

    print("after second UCSv2")
    for node in temptempGraph.nodes:
      print(node.value)
      for neighbor in node.neighbors:
        print((neighbor[0].value, neighbor[1]))
      print("--------------------")

    alg1 = UCS(temptempGraph, "V1","V4")
    path, path_length = alg1.search()
    print(" -> ".join(path))
    print(f"Length of the path: {path_length}")

if __name__ == '__main__':
  run()

# V1 -> V3 -> V4 -> V5 -> V6
# Length of the path: 6