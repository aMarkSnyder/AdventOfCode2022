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

    if not piece_no:
        initial_state = tuple([0,0,0,0,0,0,0])
    else:
        initial_state = tuple(chamber[current_depth])

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

    final_state = tuple(chamber[new_depth])
    states = tuple([initial_state,final_state])
    if v and states in cache and initial_state != final_state:
        print('possible cycle of length', piece_no-cache[states],'pieces')
    cache[states] = piece_no

    return new_depth, last_jet_idx

with open('input_test1.txt','r') as input_file:
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
for piece_no in range(300):
    current_depth,_ = drop_piece(chamber,current_depth,piece_gen,jet_gen,cache,piece_no,True)
cycle_block_length = 35 # by inspection

test_length = 8
cycle_start_depth = 0
cycle_lengths = set()
for row_idx in range(current_depth,chamber.shape[0]-test_length):
    test_array = chamber[row_idx:row_idx+test_length]
    for offset in range(test_length,chamber.shape[0]-test_length-row_idx):
        if (test_array == chamber[row_idx+offset:row_idx+offset+test_length]).all():
            print('likely cycle of height',offset)
            cycle_lengths.add(offset)
            cycle_start_depth = row_idx+test_length+offset-1
cycle_height = 53 # by inspection
print(cycle_start_depth)

elephant_requested_blocks = 1000000000000
num_cycles = elephant_requested_blocks // cycle_block_length - 10 # fudge factor since idk how many blocks the startup takes

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
