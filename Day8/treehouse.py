import numpy as np

def obscured_by(tree_height,other_trees):
    for tree in other_trees:
        if tree >= tree_height:
            return True
    return False

def visible_trees(tree_height,other_trees):
    for idx,tree in enumerate(other_trees):
        if tree >= tree_height:
            return idx+1
    return len(other_trees)

with open('input.txt','r') as input:
    input_lines = input.readlines()

trees = []
for line in input_lines:
    line = line.strip()
    trees.append([int(char) for char in line])
trees = np.array(trees)
visibility = np.zeros_like(trees)
scenic_score = np.zeros_like(trees)

height,width = trees.shape
for row in range(height):
    for col in range(width):
        if row == 0 or row == height or col == 0 or col == width:
            visibility[row,col] = 1
            scenic_score[row,col] = 0
        else:
            tree = trees[row][col]
            views = [0,0,0,0]
            side_trees = [trees[0:row,col][::-1],trees[row+1:height,col],trees[row,0:col][::-1],trees[row,col+1:width]]
            for idx,treeline in enumerate(side_trees):
                if not obscured_by(tree,treeline):
                    visibility[row,col] = 1
                views[idx] = visible_trees(tree,treeline)
            scenic_score[row,col] = np.product(views)

print(np.sum(visibility))
print(np.max(scenic_score))