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
    alg = UCSv2(graph, "V1", "V4")
    tempGraph = alg.search()
    for node in tempGraph.nodes:
      print(node.value)
      print(node.neighbors)
    # print(" -> ".join(path))
    # print(f"Length of the path: {path_length}")

if __name__ == '__main__':
  run()

# V1 -> V3 -> V4 -> V5 -> V6
# Length of the path: 6