import numpy as np

def drop_sand(current_state,max_row,min_col,max_col):
    rest = False
    curr_row,curr_col = 1,500
    while not rest:
        if curr_row == max_row:
            return 0
        if current_state[curr_row+1,curr_col] == '.':
            curr_row += 1
            continue
        if curr_col == min_col:
            return 0
        if current_state[curr_row+1,curr_col-1] == '.':
            curr_row,curr_col = curr_row+1,curr_col-1
            continue
        if curr_col == max_col:
            return 0
        if current_state[curr_row+1,curr_col+1] == '.':
            curr_row,curr_col = curr_row+1,curr_col+1
            continue
        rest = True
    current_state[curr_row,curr_col] = 'o'
    return 1

with open('input.txt','r') as input_file:
    rock_structures = input_file.readlines()
rock_structures = [rock_structure.split('->') for rock_structure in rock_structures]

rows,cols = [],[]
for rock_structure in rock_structures:
    for idx,rock_point in enumerate(rock_structure):
        col,row = rock_point.split(',')
        col,row = int(col),int(row)
        rock_structure[idx] = (col,row)
        cols.append(col)
        rows.append(row)
min_row,max_row = 0,sorted(rows)[-1]
min_col,max_col = sorted(cols)[0],sorted(cols)[-1]

current_state = np.array([['.']*(max_col+1) for _ in range(max_row+1)])
current_state[0,500] = '+'
for rock_structure in rock_structures:
    for idx,(col,row) in enumerate(rock_structure):
        if idx < len(rock_structure)-1:
            next_col,next_row = rock_structure[idx+1]
            left,right = min(col,next_col),max(col,next_col)
            top,bottom = min(row,next_row),max(row,next_row)
            current_state[top:bottom+1,left:right+1] = '#'

sand_count = 0
while drop_sand(current_state,max_row,min_col,max_col):
    sand_count += 1
print(sand_count)