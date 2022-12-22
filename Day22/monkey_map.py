import re
import numpy as np

def get_next_instrs(path,path_idx):
    return re.search(r'\d+', path[path_idx:]).group(), re.search(r'[LR]', path[path_idx:])

with open('input.txt','r',encoding='utf8') as input_file:
        input_text = input_file.read()

maze,path = input_text.split('\n\n')
maze = maze.split('\n')
maze_width = max(len(row) for row in maze)
maze = [row.ljust(maze_width) for row in maze]
maze = [[char for char in row] for row in maze]
maze = np.array(maze)

path = path.strip()

# Star 1
def find_out_of_bounds(maze,position,facing):
    match facing:
        # Check left
        case 0:
            offset = (0,-1)
        # Check up
        case 1:
            offset = (-1,0)
        # Check right
        case 2:
            offset = (0,1)
        # Check down
        case 3:
            offset = (1,0)
    oob = (position[0]+offset[0],position[1]+offset[1])
    while True:
        try:
            if maze[oob] == ' ':
                return oob
        except IndexError:
            return oob
        oob = (oob[0]+offset[0],oob[1]+offset[1])

def move_in_dir(maze,position,facing):
    match facing:
        # Right
        case 0:
            offset = (0,1)
        # Down
        case 1:
            offset = (1,0)
        # Left
        case 2:
            offset = (0,-1)
        # Up
        case 3:
            offset = (-1,0)
    goal_position = (position[0]+offset[0],position[1]+offset[1])
    try:
        match maze[goal_position]:
            case '.':
                return goal_position
            case '#':
                return position
            case ' ':
                oob = find_out_of_bounds(maze,position,facing)
                goal_position = (oob[0]+offset[0],oob[1]+offset[1])
                match maze[goal_position]:
                    case '.':
                        return goal_position
                    case '#':
                        return position
    except IndexError:
        oob = find_out_of_bounds(maze,position,facing)
        goal_position = (oob[0]+offset[0],oob[1]+offset[1])
        match maze[goal_position]:
            case '.':
                return goal_position
            case '#':
                return position

for col,val in enumerate(maze[0]):
    if val == '.':
        position = (0,col)
        break
facing = 0
path_idx = 0
while True:
    distance,turn = get_next_instrs(path,path_idx)
    if turn:
        turn = turn.group()
    path_idx += len(distance)+1
    for _ in range(int(distance)):
        position = move_in_dir(maze,position,facing)
    match turn:
        case None:
            break
        case 'L':
            facing = (facing-1) % 4
        case 'R':
            facing = (facing+1) % 4
print(1000*(position[0]+1) + 4*(position[1]+1) + facing)

# Star 2
def wrap_cube(position,facing):
    row_range = {
        1: [0],
        2: [0],
        3: range(0,50),
        4: range(0,50),
        5: [49],
        6: range(50,100),
        7: range(50,100),
        8: [100],
        9: range(100,150),
        10: range(100,150),
        11: [149],
        12: range(150,200),
        13: range(150,200),
        14: [199]
    }
    col_range = {
        1: range(50,100),
        2: range(100,150),
        3: [50],
        4: [149],
        5: range(100,150),
        6: [50],
        7: [99],
        8: range(0,50),
        9: [0],
        10: [99],
        11: range(50,100),
        12: [0],
        13: [49],
        14: range(0,50)
    }
    entry_facing = {
        1: 3,
        2: 3,
        3: 2,
        4: 0,
        5: 1,
        6: 2,
        7: 0,
        8: 3,
        9: 2,
        10: 0,
        11: 1,
        12: 2,
        13: 0,
        14: 1
    }
    row,col = position
    for edge in row_range:
        if position[0] in row_range[edge] and position[1] in col_range[edge] and facing == entry_facing[edge]:
            start_edge = edge
            break
    row_dist,col_dist = row - min(row_range[start_edge]), col - min(col_range[start_edge])
    match start_edge:
        # 1 -> 12, match order reverse dim
        case 1:
            target = 12
            goal_position = (min(row_range[target])+col_dist,min(col_range[target])+row_dist)
            new_facing = 0
        # 2 -> 14, match order match dim
        case 2:
            target = 14
            goal_position = (min(row_range[target])+row_dist,min(col_range[target])+col_dist)
            new_facing = 3
        # 3 -> 9, reverse order match dim
        case 3:
            target = 9
            goal_position = (max(row_range[target])-row_dist,max(col_range[target])-col_dist)
            new_facing = 0
        # 4 -> 10, reverse order match dim
        case 4:
            target = 10
            goal_position = (max(row_range[target])-row_dist,max(col_range[target])-col_dist)
            new_facing = 2
        # 5 -> 7, match order reverse dim
        case 5:
            target = 7
            goal_position = (min(row_range[target])+col_dist,min(col_range[target])+row_dist)
            new_facing = 2
        # 6 -> 8, match order reverse dim
        case 6:
            target = 8
            goal_position = (min(row_range[target])+col_dist,min(col_range[target])+row_dist)
            new_facing = 1
        # 7 -> 5, match order reverse dim
        case 7:
            target = 5
            goal_position = (min(row_range[target])+col_dist,min(col_range[target])+row_dist)
            new_facing = 3
        # 8 -> 6, match order reverse dim
        case 8:
            target = 6
            goal_position = (min(row_range[target])+col_dist,min(col_range[target])+row_dist)
            new_facing = 0
        # 9 -> 3, reverse order match dim
        case 9:
            target = 3
            goal_position = (max(row_range[target])-row_dist,max(col_range[target])-col_dist)
            new_facing = 0
        # 10 -> 4, reverse order match dim
        case 10:
            target = 4
            goal_position = (max(row_range[target])-row_dist,max(col_range[target])-col_dist)
            new_facing = 2
        # 11 -> 13, match order reverse dim
        case 11:
            target = 13
            goal_position = (min(row_range[target])+col_dist,min(col_range[target])+row_dist)
            new_facing = 2
        # 12 -> 1, match order reverse dim
        case 12:
            target = 1
            goal_position = (min(row_range[target])+col_dist,min(col_range[target])+row_dist)
            new_facing = 1
        # 13 -> 11, match order reverse dim
        case 13:
            target = 11
            goal_position = (min(row_range[target])+col_dist,min(col_range[target])+row_dist)
            new_facing = 3
        # 14 -> 2, match order match dim
        case 14:
            target = 2
            goal_position = (min(row_range[target])+row_dist,min(col_range[target])+col_dist)
            new_facing = 1
    return goal_position, new_facing

def move_in_dir2(maze,position,facing):
    match facing:
        # Right
        case 0:
            offset = (0,1)
        # Down
        case 1:
            offset = (1,0)
        # Left
        case 2:
            offset = (0,-1)
        # Up
        case 3:
            offset = (-1,0)
    goal_position = (position[0]+offset[0],position[1]+offset[1])
    try:
        match maze[goal_position]:
            case '.':
                return goal_position,facing
            case '#':
                return position,facing
            case ' ':
                goal_position,goal_facing = wrap_cube(position,facing)
                match maze[goal_position]:
                    case '.':
                        return goal_position,goal_facing
                    case '#':
                        return position,facing
    except IndexError:
        goal_position,goal_facing = wrap_cube(position,facing)
        match maze[goal_position]:
            case '.':
                return goal_position,goal_facing
            case '#':
                return position,facing

for col,val in enumerate(maze[0]):
    if val == '.':
        position = (0,col)
        break
facing = 0
path_idx = 0
while True:
    distance,turn = get_next_instrs(path,path_idx)
    if turn:
        turn = turn.group()
    path_idx += len(distance)+1
    for _ in range(int(distance)):
        position,facing = move_in_dir2(maze,position,facing)
    match turn:
        case None:
            break
        case 'L':
            facing = (facing-1) % 4
        case 'R':
            facing = (facing+1) % 4
print(1000*(position[0]+1) + 4*(position[1]+1) + facing)