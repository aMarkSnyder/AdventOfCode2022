import re
import numpy as np

def get_next_instrs(path,path_idx):
    return re.search(r'\d+', path[path_idx:]).group(), re.search(r'[LR]', path[path_idx:])

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