import numpy as np
from scipy.spatial import KDTree

def diffuse_elves(elves,directions,offsets,step_limit):
    step = 0
    while step < step_limit:
        elf_tree = KDTree(elves)
        next_elves = []
        proposal_elves = []
        proposals = []
        for elf in elves:
            dists,_ = elf_tree.query(elf,k=2,distance_upper_bound=1.5)
            # No elves nearby
            if dists[1] == np.inf:
                next_elves.append(elf)
            else:
                for direction in directions:
                    candidates = [(elf[0]+offset[0],elf[1]+offset[1]) for offset in offsets[direction]]
                    for candidate in candidates:
                        # Elf in that direction
                        dist,_ = elf_tree.query(candidate,distance_upper_bound=.1)
                        if dist != np.inf:
                            break
                    # If no elves in that direction
                    else:
                        proposal_elves.append(elf)
                        proposals.append(candidates[1])
                        break
                # No valid direction
                else:
                    next_elves.append(elf)
        
        if proposal_elves:
            proposal_tree = KDTree(proposals)
            for elf,proposal in zip(proposal_elves,proposals):
                dists,_ = proposal_tree.query(proposal,k=2,distance_upper_bound=.1)
                # Unique proposal
                if dists[1] == np.inf:
                    next_elves.append(proposal)
                else:
                    next_elves.append(elf)
            
        step += 1
        if set(elves) == set(next_elves):
            break
        elves = next_elves
        directions.append(directions.pop(0))

    return elves,step

with open('input.txt','r',encoding='utf8') as input_file:
        initial_state = input_file.readlines()

offsets = {
    'N': [(-1,-1),(-1,0),(-1,1)],
    'S': [(1,-1),(1,0),(1,1)],
    'W': [(-1,-1),(0,-1),(1,-1)],
    'E': [(-1,1),(0,1),(1,1)]
}
elves = []
for row_idx,row in enumerate(initial_state):
    for col_idx,val in enumerate(row):
        if val == '#':
            elves.append((row_idx,col_idx))

# Star 1
final_elves,_ = diffuse_elves(elves,directions=['N','S','W','E'],offsets=offsets,step_limit=10)
min_x,min_y = np.inf,np.inf
max_x,max_y = -np.inf,-np.inf
for elf in final_elves:
    min_x,min_y = min(min_x,elf[0]), min(min_y,elf[1])
    max_x,max_y = max(max_x,elf[0]), max(max_y,elf[1])
area = (max_x-min_x+1) * (max_y-min_y+1)
print(area - len(final_elves))

# Star 2
_, final_step = diffuse_elves(elves,directions=['N','S','W','E'],offsets=offsets,step_limit=np.inf)
print(final_step)