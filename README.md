# PathFinding_NYC

## Problem statement
1. Given a graph of nodes and edges and a start and ending node. Find the shortest path from start to end.
2. Given the same graph but with new values for each edge (previously distance, now with distance and fuel cost), find the shortest path from start to end while complying to the fuel limit.
3. Use a informed search algorithm to do the same as above.

## Solution
1. Perform basic UCS
2. Modify UCS which checks if neighboring node of current node has been placed in queue, if it has then check if fuel left is more than same node in queue, if it has more than include this node and path into the queue.
3. Modify the Astar algorithm to include more nodes into its queue, while taking into account the heuristic cost -> calculated using the euclidean distance of coordinates of current node and ending node.
