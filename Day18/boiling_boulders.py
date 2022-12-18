import re
import numpy as np

def surface_area(grid):
    surface_faces = 0

    axis_size = grid.shape[0]
    axis_surface_faces = 0
    for idx in range(axis_size):
        if idx == 0:
            axis_surface_faces += np.sum(grid[idx,:,:])
        else:
            axis_surface_faces += np.sum((grid[idx,:,:]-grid[idx-1,:,:]) != 0)
            if idx == axis_size-1:
                axis_surface_faces += np.sum(grid[idx,:,:])
    surface_faces += axis_surface_faces
    print(axis_surface_faces,'from x axis')

    axis_size = grid.shape[1]
    axis_surface_faces = 0
    for idx in range(axis_size):
        if idx == 0:
            axis_surface_faces += np.sum(grid[:,idx,:])
        else:
            axis_surface_faces += np.sum((grid[:,idx,:]-grid[:,idx-1,:]) != 0)
            if idx == axis_size-1:
                axis_surface_faces += np.sum(grid[:,idx,:])
    surface_faces += axis_surface_faces
    print(axis_surface_faces,'from y axis')

    axis_size = grid.shape[2]
    axis_surface_faces = 0
    for idx in range(axis_size):
        if idx == 0:
            axis_surface_faces += np.sum(grid[:,:,idx])
        else:
            axis_surface_faces += np.sum((grid[:,:,idx]-grid[:,:,idx-1]) != 0)
            if idx == axis_size-1:
                axis_surface_faces += np.sum(grid[:,:,idx])
    surface_faces += axis_surface_faces
    print(axis_surface_faces,'from z axis')

    return surface_faces

with open('input_test1.txt','r') as input_file:
    points = input_file.readlines()

locations = np.zeros((len(points),3),dtype=int)
for idx,point in enumerate(points):
    locations[idx] = [int(coord) for coord in re.findall(r'\d+', point)]

grid = np.zeros(tuple(np.max(locations,axis=0)+1))
print('grid shape is',grid.shape)
for location in locations:
    grid[tuple(location)] = 1

print(surface_area(grid))

