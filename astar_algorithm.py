from queue import PriorityQueue
from graph import Node, Graph
import math

class Astar:
  """
    This class used to represent the Greedy algorithm
    ...
    Attributes
    ----------
    graph : Graph
      Represent the graph (search space of the problem) 
    start : str
      Represent the starting point 
    target : str
      Represent the destination (target) node
    opened : list
      Represent the list with the available nodes in the search process
    closed : list
      Represent the list with the closed (visited) nodes
    number_of_steps : int
      Keep the number of steps of the algorithm
    ...
    Methods
    -------
    calculate_distance(self, parent, child) -> int
      Calculate the distance from the starting node to the child node
    insert_to_list(self, list_category, node) -> None
      Insert a new node either ot opened or to closed list according to list_category parameter 
    remove_from_opened(self) -> Node
      Remove from the opened list the node with the smallest heuristic value
    opened_is_empty(self) -> Boolean
      Check if the opened list is empty or not
    get_old_node(self, node_value) -> Node
      Return the node from the opened list in case of a new node with the same value
    calculate_path(self, target_node) -> list
      Calculate and return the path from the stat node to target node
    search(self)
        Implements the core of algorithm. This method searches, in the search space of the problem, a solution 
    """

  def __init__ (self, graph, distDict, costDict, coordDict start_position, target):
    self.graph = graph
    self.start = graph.find_node(start_position)
    self.target = graph.find_node(target)
    self.opened = []
    self.closed = []
    self.number_of_steps = 0
    self.distDict = distDict
    self.costDict = costDict
    self.coordDict = coordDict


  def calculate_distance(self, parent, child):
    """
      Calculate and return the distance from the start to child node. If the heuristic value has already calculated
      and is smaller than the new value, the method return theold value. Otherwise the method return the new value
      and note the parent as the parent node of child
      Parameters
      ----------
      parent : Node
        Represent the parent node
      child : Node
        Represent the child node
      ...
      Return 
      ------
        int
    """
    for neighbor in parent.neighbors:
      if neighbor[0] == child:
        distance = parent.heuristic_value + neighbor[1]
        if distance < child.heuristic_value:
          child.parent = parent
          return distance
        
        return child.heuristic_value

  
  def insert_to_list(self, list_category, node):
    """
      Insert a node in the proper list (opened or closed) according to list_category
      Parameters
      ----------
      list_category : str
          Determines the list in which the node will be appened. If the value is 'open' 
          the node is appended in the opened list. Otherwise, the node is appended in the closed list
      node : Node
          The node of the problem that will be added to the frontier
    """
    if list_category == "open":
      self.opened.append(node)
    else:
      self.closed.append(node)
  

  def remove_from_opened(self):
    """
      Remove the node with the smallest heuristic value from the opened list
      Then add the removed node to the closed list
      Returns
      -------
        Node
    """
    self.opened.sort()
    # for n in self.opened:
    #   print(f"({n},{n.heuristic_value})", end = " ")
    # print("\n")
    node = self.opened.pop(0)
    self.closed.append(node)
    return node


  def opened_is_empty(self):
    """
      Check if the the list opened is empty, so no solution found
      Returns
      -------
      Boolean
        True if the list opened is empty
        False if the list opened is not empty
    """
    return len(self.opened) == 0


  def get_old_node(self, node_value):
    """
      Return the node with the given value from the opened list,
      to compare its heuristic_value with a node with the same value
      ...
      Parameters
      ----------
        node_value : Node
        Represent the value of the node
      Returns
      -------
        Node
    """
    for node in self.opened:
      if node.value == node_value:
        return node
    return None 
      

  def calculate_path(self, target_node):
    """
      Calculate and return the path (solution) of the problem
      ...
      Parameters
      ----------
        target_node : Node
        Represent final (destination) node of the problem
      Returns
      -------
        list
    """
    path = [target_node.value]
    node = target_node.parent
    while True:
      path.append(node.value)
      if node.parent is None:
        break
      node = node.parent
    path.reverse()
    return path
  
  def get_h_value(self,node_value):
    x,y = self.coordDict['50']
    a,b = self.coordDict[node_value]
    h_value=math.sqrt(pow((x-a),2) + pow((y-b),2))
    return h_value

  def search(self):
    """
      Is the main algorithm. Search for a solution in the solution space of the problem
      Stops if the opened list is empty, so no solution found or if it find a solution. 
      ...
      Return
      ------
        list
    """
    # The heuristic value of the starting node is zero
    #self.start.heuristic_value = 0
    # Add the starting point to opened list
    count = 0
    open_set = PriorityQueue()
    #get heuristic value
    h_initial = self.get_h_value('0')
    open_set.put((h_initial, count, self.start, self.start, 14)) #fuel limit of 14
    tempGraph = Graph()
    tempGraph.add_node(Node(self.start.value))
    

    while not open_set.empty():
      self.number_of_steps += 1
      current = open_set.get() #grab the highest priority node
      #about to expand current
      #add current to answer graph, tempGraph
      if self.number_of_steps>1:
        if tempGraph.find_node(current[2].value) == None:
          tempGraph.add_node(Node(current[2].value))
        node2Value = current[2].value
        node1Value = current[3].value
        stringValues = f'{node1Value},{node2Value}'
        if not tempGraph.are_connected(node1Value, node2Value):
          tempGraph.add_edge(current[3], current[2], self.distDict[stringValues]) #bi directional graph, edge will be added in both node

      # print(f"Selected Node {selected_node}")
      # check if the selected_node is the solution
      if current[2] == self.target: #comparing node to node
        return tempGraph

      # extend the node, return list of neighbors
      new_nodes = current[2].extend_node()

      # add the extended nodes in the list opened
      if len(new_nodes) > 0:
        for new_node in new_nodes:
          node1Value = current[2].value
          node2Value = new_node.value
          stringValues = f'{node1Value},{node2Value}'
          tempScore = current[0] + self.distDict[stringValues]
          h_value = self.get_h_value(str(node2Value))
          finalScore = tempScore+h_value
          fuelLeft = current[4] - self.costDict[stringValues]
          if fuelLeft < 0: #should not take this path
            continue
          else:
            count+=1
            open_set.put((finalScore, count, new_node, current[2], fuelLeft))