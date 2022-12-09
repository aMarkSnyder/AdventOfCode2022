def move_up(head,tail):
    head[1] += 1
    if head[1]-tail[1] > 1:
        tail[0] = head[0]
        tail[1] = head[1]-1

def move_down(head,tail):
    head[1] -= 1
    if tail[1]-head[1] > 1:
        tail[0] = head[0]
        tail[1] = head[1]+1

def move_left(head,tail):
    head[0] -= 1
    if tail[0]-head[0] > 1:
        tail[1] = head[1]
        tail[0] = head[0]+1

def move_right(head,tail):
    head[0] += 1
    if head[0]-tail[0] > 1:
        tail[1] = head[1]
        tail[0] = head[0]-1

with open('input.txt','r') as input:
    input_lines = input.read().splitlines()

directions = ['U','D','L','R']
move_fns = [move_up,move_down,move_left,move_right]

tail_locations = set([(0,0)])
head = [0,0]
tail = [0,0]
for line in input_lines:
    direction,magnitude = line.split()
    magnitude = int(magnitude)
    move_fn = move_fns[directions.index(direction)]
    for _ in range(magnitude):
        move_fn(head,tail)
        tail_locations.add(tuple(tail))

print(len(tail_locations))