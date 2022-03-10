from queue import PriorityQueue
  

class UCS:

  def __init__(self, gDict, distDict, start_position, target):
    self.gDict = gDict
    self.distDict = distDict
    self.start = start_position
    self.target = target
    self.number_of_steps = 0
      

  def calculate_path(self, target_node, parentDict):
    path = [target_node]
    node = parentDict[target_node]
    while True:
      path.append(node)
      if parentDict[node] is None: #start found
        break
      node = parentDict[node]
    path.reverse()
    return path
  

  def search(self):

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, self.start))
    parentDict = {} # keeps track of the parent of each node that results in smallest gScore
    parentDict[self.start] = None
    gScore = {}
    gScore[self.start] = 0
    visited = []

    while not open_set.empty():
      self.number_of_steps += 1
      
      selected_node = open_set.get()
      visited.append(selected_node) #keeps track of nodes that we have alr visited
      # check if the selected_node is the solution
      if selected_node[2] == self.target:
        path = self.calculate_path(selected_node[2], parentDict) #pass the end and parentDict to find the path
        return path, self.number_of_steps

      # extend the node
      new_nodes = self.gDict[selected_node[2]]

      # add the extended nodes in the list opened
      if len(new_nodes) > 0:
        for new_node in new_nodes:
          stringValues = f'{new_node},{selected_node[2]}'
          tempGScore = self.distDict[stringValues] + gScore[selected_node[2]]
          if new_node not in visited and new_node not in parentDict.keys(): #parent.keys() is a list of node that has been put into priority queue
            count+=1
            #update gScore
            gScore[new_node] = tempGScore
            open_set.put((gScore[new_node], count, new_node))
            #update parentDict
            parentDict[new_node] = selected_node[2]
          
          elif new_node in parentDict.keys() and new_node not in visited and parentDict[new_node] != selected_node:
            oldGScore = gScore[new_node]
            if tempGScore < oldGScore:
              parentDict[new_node] = selected_node[2]
              gScore[new_node] = tempGScore





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
    pathList = []
    pathList.append(self.start)
    open_set.put((0, count, self.start, self.start, 287932, pathList)) #fuel limit of 287932
    tempGDict = {}
    tempGDict[self.start] = []
    maxFuelLeft = {}
    maxFuelLeft[self.start] = 287932
    expansionCount = 0

    while not open_set.empty():
      current = open_set.get() #grab the highest priority node
      expansionCount += 1
      #print(current)
      #about to expand current
      #add current to answer graph, tempGraph
      # if current[2] != self.start:
      #   if current[2] not in tempGDict.keys():
      #     tempGDict[current[2]] = []
      #   node2Value = current[2]
      #   node1Value = current[3]
      #   stringValues = f'{node1Value},{node2Value}'
      #   if node1Value not in tempGDict[current[2]]:
      #     tempGDict[current[2]].append(node1Value) #bi directional graph, edge will be added in both node
      #   if node2Value not in tempGDict[current[3]]:
      #     tempGDict[current[3]].append(node2Value)

      # check if the selected_node is the solution
      if current[2] == self.target: #comparing string to string
        return current[5], expansionCount #return path

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
          
          if new_node not in maxFuelLeft.keys() or maxFuelLeft[new_node] < fuelLeft:
            maxFuelLeft[new_node] = fuelLeft
            count+=1
            newPath = current[5].copy() #take a copy of the list
            if new_node in newPath: continue
            newPath.append(new_node)
            open_set.put((tempScore, count, str(new_node), current[2], fuelLeft, newPath))
            self.edgeDict[stringValues] = 1
            self.edgeDict[flippedStringValues] = 1

class UCSv3:

  def __init__(self, gDict, distDict, start_position, target, costDict):
    self.gDict = gDict
    self.distDict = distDict
    self.start = start_position
    self.target = target
    self.number_of_steps = 0
    self.costDict=costDict
      

  def calculate_path(self, target_node, parentDict):
    path = [target_node]
    node = parentDict[target_node]
    while True:
      path.append(node)
      if parentDict[node] is None: #start found
        break
      node = parentDict[node]
    path.reverse()
    return path
  
  def update_pq(self,open_set,newGScore,count,node):
    temp=PriorityQueue()
    for i in open_set.queue:
      if i[2]==node:
        temp.put((newGScore,count,node))
      else:
        temp.put(i)
    return temp
        


  def search(self):

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, self.start, list(self.start),287932))
    parentDict = {} # keeps track of the parent of each node that results in smallest gScore
    parentDict[self.start] = None
    gScore = {}
    gScore[self.start] = 0
    visited = []
    closed_dict = {} #dict to store the lowest fuel cost to each node
    while not open_set.empty():
      self.number_of_steps += 1
      selected_node = open_set.get()
      # print('fuel:',selected_node[4])
      # update closed dict to new value of fuel which will allow for future lower fuel alt to be added to pq
      closed_dict[selected_node[2]]=selected_node[4]
      visited.append(selected_node) #keeps track of nodes that we have alr visited
      
      # check if the selected_node is the solution
      if selected_node[2] == self.target:
        return selected_node

      # extend the node
      new_nodes = self.gDict[selected_node[2]]

      # add the extended nodes in the list opened
      if len(new_nodes) > 0:
        for new_node in new_nodes:
          # print('new_node',new_node)
          stringValues = f'{new_node},{selected_node[2]}'
          tempGScore = self.distDict[stringValues] + selected_node[0]
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
          open_set.put((tempGScore, count, new_node , new_route ,tempFuelLeft))
