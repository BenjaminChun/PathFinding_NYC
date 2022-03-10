import math
from queue import PriorityQueue
from select import select
  

class Astar:

  def __init__(self, gDict, distDict, start_position, target, costDict, coordDict):
    self.gDict = gDict
    self.distDict = distDict
    self.start = start_position
    self.target = target
    self.number_of_steps = 0
    self.costDict=costDict
    self.coordDict=coordDict

  def get_h_value(self,node_value):
    x,y = self.coordDict[self.target]
    a,b = self.coordDict[node_value]
    h_value=math.sqrt(pow((x-a),2) + pow((y-b),2))
    return h_value

  def search(self):
    count=0
    open_set = PriorityQueue()
    initial_h=self.get_h_value(self.start)
    open_set.put((initial_h, count, self.start, list(self.start),287932))
    closed_dict = {} #dict to store the lowest fuel cost to each node
    while not open_set.empty():
      self.number_of_steps += 1
      selected_node = open_set.get()
      # print('fuel:',selected_node[4])
      # update closed dict to new value of fuel which will allow for future lower fuel alt to be added to pq
      closed_dict[selected_node[2]]=selected_node[4]
  
      # check if the selected_node is the solution
      if selected_node[2] == self.target:
        return selected_node,self.number_of_steps

      # extend the node
      new_nodes = self.gDict[selected_node[2]]

      # add the extended nodes in the list opened
      if len(new_nodes) > 0:
        for new_node in new_nodes:
          # print('new_node',new_node)
          stringValues = f'{new_node},{selected_node[2]}'
          tempGScore = self.distDict[stringValues] + selected_node[0]-self.get_h_value(selected_node[2])
          hScore = self.get_h_value(new_node)
          tempFinalScore = tempGScore+hScore
          tempFuelLeft = selected_node[4] - self.costDict[stringValues]
          if new_node in closed_dict:
            # check if fuel is less than recorded as of current path
            # only update if remaining fuel is more and dist covered is more
            # if remaining fuel is less and dist covered is more then dont need to bother
            if tempFuelLeft<closed_dict[new_node]:
              continue
            else:
              closed_dict[new_node] = tempFuelLeft
          # check if fuel is less than 0
          if tempFuelLeft<0:
            continue
          # if path goes back to itself (shldnt happen) discard it
          new_route = selected_node[3].copy()
          if str(new_node) in new_route:
            continue

          # add new_node to new_route
          new_route.append(new_node)
          # print(new_node)
          # print(tempGScore, count, new_node , new_route ,tempFuelLeft)
          #passed all tests and add to openset to be popped
          open_set.put((tempFinalScore, count, new_node , new_route ,tempFuelLeft))
              





class UCSv2:
  
  def __init__(self, gDict, distDict, costDict, start_position, target):
    self.gDict = gDict
    self.start = start_position #string
    self.target = target #string
    self.opened = []
    self.closed = []
    self.number_of_steps = 0
    self.distDict = distDict
    self.costDict = costDict
    self.edgeDict = {}

  def search(self):
    
    # The heuristic value of the starting node is zero
    #self.start.heuristic_value = 0
    # Add the starting point to opened list
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, self.start, self.start, 287932)) #fuel limit of 287932
    tempGDict = {}
    tempGDict[self.start] = []



    while not open_set.empty():
      current = open_set.get() #grab the highest priority node
      print(current)
      #about to expand current
      #add current to answer graph, tempGraph
      if current[2] != self.start:
        if current[2] not in tempGDict.keys():
          tempGDict[current[2]] = []
        node2Value = current[2]
        node1Value = current[3]
        stringValues = f'{node1Value},{node2Value}'
        if node1Value not in tempGDict[current[2]]:
          tempGDict[current[2]].append(node1Value) #bi directional graph, edge will be added in both node
        if node2Value not in tempGDict[current[3]]:
          tempGDict[current[3]].append(node2Value)

      # check if the selected_node is the solution
      if current[2] == self.target: #comparing string to string
        print('Done')
        return tempGDict

      # extend the node, return list of neighbors
      new_nodes = self.gDict[current[2]]
      #print(new_nodes)

      # add the extended nodes in the list opened
      if len(new_nodes) > 0:
        for new_node in new_nodes:
          if new_node == current[3]: continue
          node1Value = current[2]
          node2Value = new_node
          #print(node2Value)
          stringValues = f'{node1Value},{node2Value}'
          flippedStringValues = f'{node2Value},{node1Value}'
          #print(stringValues)
          tempScore = current[0] + self.distDict[stringValues]
          fuelLeft = current[4] - self.costDict[stringValues]
          if fuelLeft < 0: #should not take this path
            continue
          else:
            if stringValues not in self.edgeDict.keys():
              count+=1
              open_set.put((tempScore, count, str(new_node), current[2], fuelLeft))
              self.edgeDict[stringValues] = 1
              self.edgeDict[flippedStringValues] = 1
