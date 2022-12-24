from collections import defaultdict,deque
import numpy as np

def advance_blizzards(blizzards,offsets,height,width):
	new_blizzards = defaultdict(list)
	for loc,directions in blizzards.items():
		for direction in directions:
			proposal = loc+offsets[direction]
			if proposal[0] == 0:
					proposal[0] = height-2
			elif proposal[0] == height-1:
					proposal[0] = 1
			elif proposal[1] == 0:
					proposal[1] = width-2
			elif proposal[1] == width-1:
					proposal[1] = 1
			new_blizzards[tuple(proposal)].append(direction)
	return new_blizzards

def steps_to_goal(blizzards,start,goal,offsets,height,width):
	blizzards = advance_blizzards(blizzards,offsets,height,width)
	q = deque()
	curr_step = 0
	q.append((start,0))
	while q:
		curr_pos,step = q.popleft()
		if curr_pos == goal:
			break
		if step != curr_step:
			blizzards = advance_blizzards(blizzards,offsets,height,width)
			curr_step += 1
		for offset in offsets.values():
			proposal = tuple(curr_pos + offset)
			if proposal == start:
				q.append((proposal,step+1))
			if proposal == goal:
				step += 1
				q = None
				break
			if 1 <= proposal[0] < height-1 and 1 <= proposal[1] < width-1 and proposal not in blizzards and (proposal,step+1) not in q:
				q.append((proposal,step+1))
	return step, blizzards

with open('input.txt','r',encoding='utf8') as input_file:
        initial_state = input_file.readlines()
initial_state = [[char for char in line.strip()] for line in initial_state]

height,width = np.array(initial_state).shape
start = (0,1)
finish = (height-1,width-2)
offsets = {
    '<': np.array([0,-1]),
    '>': np.array([0,1]),
    '^': np.array([-1,0]),
    'v': np.array([1,0]),
	's': np.array([0,0])
}
blizzards = defaultdict(list)
for row_idx,row in enumerate(initial_state):
    for col_idx,val in enumerate(row):
        if val in '<>^v':
            blizzards[(row_idx,col_idx)].append(val)

part1_steps,blizzards = steps_to_goal(blizzards,start,finish,offsets,height,width)
print(part1_steps)

steps_back,blizzards = steps_to_goal(blizzards,finish,start,offsets,height,width)
final_steps,_ = steps_to_goal(blizzards,start,finish,offsets,height,width)
print(part1_steps+steps_back+final_steps)