import re
import numpy as np

# Star 1
def surface_area(grid):
    surface_faces = 0

    axis_size = grid.shape[0]
    axis_surface_faces = 0
    for idx in range(axis_size):
        axis_surface_faces += np.sum((grid[idx,:,:]-grid[idx-1,:,:]) != 0)
    surface_faces += axis_surface_faces
    print(axis_surface_faces,'from x axis')

    axis_size = grid.shape[1]
    axis_surface_faces = 0
    for idx in range(axis_size):
        axis_surface_faces += np.sum((grid[:,idx,:]-grid[:,idx-1,:]) != 0)
    surface_faces += axis_surface_faces
    print(axis_surface_faces,'from y axis')

    axis_size = grid.shape[2]
    axis_surface_faces = 0
    for idx in range(axis_size):
        axis_surface_faces += np.sum((grid[:,:,idx]-grid[:,:,idx-1]) != 0)
    surface_faces += axis_surface_faces
    print(axis_surface_faces,'from z axis')

    return surface_faces

with open('input.txt','r') as input_file:
    points = input_file.readlines()

locations = np.zeros((len(points),3),dtype=int)
# Adding 1 to coords ensures there will be air around the edge of the grid, eliminating edge cases
for idx,point in enumerate(points):
    locations[idx] = [int(coord)+1 for coord in re.findall(r'\d+', point)]

# Same elimination of edge cases on the other side
grid = np.zeros(tuple(np.max(locations,axis=0)+2))
for location in locations:
    grid[tuple(location)] = 1

print(surface_area(grid))

# Star 2
def get_neighbors(grid,coords):
    neighbor_coords = []
    candidates = [
        (coords[0]-1,coords[1],coords[2]),
        (coords[0]+1,coords[1],coords[2]),
        (coords[0],coords[1]-1,coords[2]),
        (coords[0],coords[1]+1,coords[2]),
        (coords[0],coords[1],coords[2]-1),
        (coords[0],coords[1],coords[2]+1)
    ]
    for candidate in candidates:
        try:
            if not grid[candidate]:
                neighbor_coords.append(candidate)
        except IndexError:
            pass
    return neighbor_coords

def BFS(grid, start):
    queue = [start]
    explored = set([start])
    distances = np.inf * np.ones_like(grid)
    distances[start] = 0
    while queue:
        point = queue.pop(0)
        neighbors = get_neighbors(grid,point)
        for neighbor in neighbors:
            if neighbor not in explored:
                explored.add(neighbor)
                distances[neighbor] = distances[point] + 1
                queue.append(neighbor)
    return distances

def external_surface_area(grid,external):
    surface_faces = 0

    axis_size = grid.shape[0]
    axis_surface_faces = 0
    for idx in range(axis_size):
        slice_diff = grid[idx,:,:]-grid[idx-1,:,:]
        for row in range(slice_diff.shape[0]):
            for col in range(slice_diff.shape[1]):
                if slice_diff[row,col] == 1 and external[(idx-1,row,col)]:
                    axis_surface_faces += 1
                elif slice_diff[row,col] == -1 and external[(idx,row,col)]:
                    axis_surface_faces += 1
    surface_faces += axis_surface_faces
    print(axis_surface_faces,'from x axis')

    axis_size = grid.shape[1]
    axis_surface_faces = 0
    for idx in range(axis_size):
        slice_diff = grid[:,idx,:]-grid[:,idx-1,:]
        for row in range(slice_diff.shape[0]):
            for col in range(slice_diff.shape[1]):
                if slice_diff[row,col] == 1 and external[(row,idx-1,col)]:
                    axis_surface_faces += 1
                elif slice_diff[row,col] == -1 and external[(row,idx,col)]:
                    axis_surface_faces += 1
    surface_faces += axis_surface_faces
    print(axis_surface_faces,'from y axis')

    axis_size = grid.shape[2]
    axis_surface_faces = 0
    for idx in range(axis_size):
        slice_diff = grid[:,:,idx]-grid[:,:,idx-1]
        for row in range(slice_diff.shape[0]):
            for col in range(slice_diff.shape[1]):
                if slice_diff[row,col] == 1 and external[(row,col,idx-1)]:
                    axis_surface_faces += 1
                elif slice_diff[row,col] == -1 and external[(row,col,idx)]:
                    axis_surface_faces += 1
    surface_faces += axis_surface_faces
    print(axis_surface_faces,'from z axis')

    return surface_faces

# Only air spaces can be external
external = BFS(grid,(0,0,0)) != np.inf
print(external_surface_area(grid,external))