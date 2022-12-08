import numpy as np

def obscured_by(tree_height,other_trees):
    for tree in other_trees:
        if tree >= tree_height:
            return True
    return False

with open('input.txt','r') as input:
    input_lines = input.readlines()

trees = []
for line in input_lines:
    line = line.strip()
    trees.append([int(char) for char in line])
trees = np.array(trees)
visibility = np.zeros_like(trees)

height,width = trees.shape
for row in range(height):
    for col in range(width):
        if row == 0 or row == height or col == 0 or col == width:
            visibility[row,col] = 1
        else:
            tree = trees[row][col]
            if not obscured_by(tree,trees[0:row,col]):
                visibility[row][col] = 1
                continue
            if not obscured_by(tree,trees[row+1:height,col]):
                visibility[row][col] = 1
                continue
            if not obscured_by(tree,trees[row,0:col]):
                visibility[row][col] = 1
                continue
            if not obscured_by(tree,trees[row,col+1:width]):
                visibility[row][col] = 1
                continue

print(np.sum(visibility))