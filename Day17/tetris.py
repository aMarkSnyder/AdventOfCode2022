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
        yield pieces[count % 5]
        count += 1

def jet_generator(jets):
    num_jets = len(jets)
    count = 0
    while True:
        yield 1 if jets[count % num_jets] == '>' else -1
        count += 1

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

def drop_piece(chamber,current_depth,piece_gen,jet_gen):

    start_point = np.array((current_depth-4,2))
    piece = next(piece_gen)

    current_spaces = [tuple(start_point+offset) for offset in piece]
    new_depth = current_depth-4+min([offset[0] for offset in piece])
    while True:
        jet = next(jet_gen)
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

    return new_depth

np.set_printoptions(linewidth=100)

with open('input.txt','r') as input_file:
    jets = input_file.readlines()[0][:-1]

piece_gen = piece_generator()
jet_gen = jet_generator(jets)

chamber = np.zeros((10000,7))
current_depth = 10000
for piece_no in range(2022):
    current_depth = drop_piece(chamber,current_depth,piece_gen,jet_gen)
print(10000-current_depth)