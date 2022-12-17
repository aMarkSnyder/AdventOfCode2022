import numpy as np

def piece_generator():
    piece1 = [(0,0),(0,1),(0,2),(0,3)]
    piece2 = [(-1,0),(0,1),(-1,1),(-2,1),(-1,2)]
    piece3 = [(0,0),(0,1),(0,2),(-1,2),(-2,2)]
    piece4 = [(0,0),(-1,0),(-2,0),(-3,0)]
    piece5 = [(0,0),(0,1),(-1,0),(-1,1)]
    pieces = [piece1,piece2,piece3,piece4,piece5]
    count = 0
    while True:
        yield pieces[count],count
        count = (count+1) % 5

def jet_generator(jets):
    num_jets = len(jets)
    count = 0
    while True:
        value = 1 if jets[count] == '>' else -1
        yield value,count
        count = (count+1) % num_jets

def valid(chamber,candidate_places):
    try:
        for place in candidate_places:
            if not 0 <= place[1] < 7:
                return False
            if chamber[place]:
                return False
    except:
        return False
    return True

def drop_piece(chamber,current_depth,piece_gen,jet_gen,cache,piece_no,v=False):

    start_point = np.array((current_depth-4,2))
    piece,_ = next(piece_gen)

    current_spaces = [tuple(start_point+offset) for offset in piece]
    new_depth = current_depth-4+min([offset[0] for offset in piece])
    while True:
        jet,last_jet_idx = next(jet_gen)
        next_spaces = [tuple([space[0],space[1]+jet]) for space in current_spaces]
        if valid(chamber,next_spaces):
            current_spaces = next_spaces
        next_spaces = [tuple([space[0]+1,space[1]]) for space in current_spaces]
        if valid(chamber,next_spaces):
            current_spaces = next_spaces
            new_depth = min(new_depth+1,current_depth)
        else:
            break
    for space in current_spaces:
        chamber[space] = 1

    if chamber.shape[0]-new_depth >= 20:
        state = str(chamber[new_depth:new_depth+20])
        if v and state in cache:
            print('possible cycle of length', piece_no-cache[state],'pieces detected at piece number',piece_no \
                ,'and old piece number',cache[state])
        cache[state] = piece_no

    return new_depth, last_jet_idx

with open('input.txt','r') as input_file:
    jets = input_file.readlines()[0][:-1]

piece_gen = piece_generator()
jet_gen = jet_generator(jets)

chamber = np.zeros((10000,7))
current_depth = 10000
cache = {}
for piece_no in range(2022):
    current_depth,_ = drop_piece(chamber,current_depth,piece_gen,jet_gen,cache,piece_no)
print(10000-current_depth)

# Star 2
piece_gen = piece_generator()
jet_gen = jet_generator(jets)
chamber = np.zeros((10000,7))
current_depth = 10000
cache = {}
depths = []
for piece_no in range(2500):
    current_depth,_ = drop_piece(chamber,current_depth,piece_gen,jet_gen,cache,piece_no,v=False)
    depths.append(current_depth)
cycle_block_length = 1705 # by inspection with verbose flag above
cycle_height = depths[626]-depths[2331] # by inspection

elephant_requested_blocks = 1000000000000
num_cycles = elephant_requested_blocks // cycle_block_length - 2 # fudge factor

blocks_remaining = elephant_requested_blocks - num_cycles*cycle_block_length

piece_gen = piece_generator()
jet_gen = jet_generator(jets)
chamber = np.zeros((10000,7))
current_depth = 10000
cache = {}
for piece_no in range(blocks_remaining):
    current_depth,_ = drop_piece(chamber,current_depth,piece_gen,jet_gen,cache,piece_no)
extra_height = 10000-current_depth

print(num_cycles*cycle_height+extra_height)
