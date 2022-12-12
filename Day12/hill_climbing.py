from heapq import *
import itertools
import numpy as np

REMOVED = '<removed-node>'      # placeholder for a removed node
counter = itertools.count()     # unique sequence count

def add_node(pq, entry_finder, counter, node, distance=0):
    'Add a new node or update the distance of an existing node'
    if node in entry_finder:
        remove_node(entry_finder,node)
    count = next(counter)
    entry = [distance, count, node]
    entry_finder[node] = entry
    heappush(pq, entry)

def remove_node(entry_finder, node):
    'Mark an existing node as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(node)
    entry[-1] = REMOVED

def pop_node(pq, entry_finder):
    'Remove and return the lowest distance node. Raise KeyError if empty.'
    while pq:
        distance, count, node = heappop(pq)
        if node is not REMOVED:
            del entry_finder[node]
            return distance,node
    raise KeyError('pop from an empty priority queue')

def get_neighbors(heights,node):
    height,width = heights.shape
    node = np.array(node)
    neighbors = []
    for offset in [[-1,0],[0,-1],[1,0],[0,1]]:
        neighbor = node + offset
        if 0 <= neighbor[0] < height and 0 <= neighbor[1] < width:
            neighbors.append(tuple(neighbor))
    
    node = tuple(node)
    distances = []
    for neighbor in neighbors:
        distance = heights[neighbor] - heights[node]
        if distance > 1:
            distance = np.inf
        else:
            distance = 1
        distances.append(distance)

    sorted_idxs = np.argsort(distances)
    neighbors = [neighbors[idx] for idx in sorted_idxs]
    distances = [distances[idx] for idx in sorted_idxs]
    
    return neighbors,distances

# function Dijkstra(Graph, source):
#  2      
#  3      for each vertex v in Graph.Vertices:
#  4          dist[v] ← INFINITY
#  5          prev[v] ← UNDEFINED
#  6          add v to Q
#  7      dist[source] ← 0
#  8      
#  9      while Q is not empty:
# 10          u ← vertex in Q with min dist[u]
# 11          remove u from Q
# 12          
# 13          for each neighbor v of u still in Q:
# 14              alt ← dist[u] + Graph.Edges(u, v)
# 15              if alt < dist[v]:
# 16                  dist[v] ← alt
# 17                  prev[v] ← u
# 18
# 19      return dist[], prev[]

def Dijkstra(heights, source):

    distances = np.inf*np.ones_like(heights)
    distances[source] = 0
    previous = np.zeros_like(heights,dtype=object)

    queue = []
    entry_finder = {}
    for row_idx,row in enumerate(distances):
        for col_idx,distance in enumerate(row):
            node = (row_idx,col_idx)
            add_node(queue,entry_finder,counter,node,distance)

    while queue:
        try:
            closest_dist,closest_node = pop_node(queue,entry_finder)
        except:
            break

        neighbors, neighbor_dists = get_neighbors(heights,closest_node)
        for neighbor,neighbor_dist in zip(neighbors,neighbor_dists):
            if neighbor not in entry_finder:
                continue
            alt = closest_dist + neighbor_dist
            if alt < distances[neighbor]:
                add_node(queue,entry_finder,counter,neighbor,alt)
                distances[neighbor] = alt
                previous[neighbor] = closest_node

    return distances,previous
    
heights = []
with open('input.txt','r') as input:
    for lineidx,line in enumerate(input):
        charnums = [ord(char)-ord('a') for char in line.strip()]
        for idx,charnum in enumerate(charnums):
            if charnum == ord('S')-ord('a'):
                start = (lineidx,idx)
                charnums[idx] = 0
            elif charnum == ord('E')-ord('a'):
                end = (lineidx,idx)
                charnums[idx] = 25
        heights.append(charnums)
heights = np.array(heights)

# Star 1
distances,previous = Dijkstra(heights,start)
print(distances[end])