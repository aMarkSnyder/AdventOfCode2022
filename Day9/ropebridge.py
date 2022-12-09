from math import copysign

def chase(target,segment):
    hori_dist = target[0] - segment[0]
    vert_dist = target[1] - segment[1]
    if abs(hori_dist) > 1:
        segment[0] += copysign(1,hori_dist)
        if vert_dist:
            segment[1] += copysign(1,vert_dist)
    elif abs(vert_dist) > 1:
        segment[1] += copysign(1,vert_dist)
        if hori_dist:
            segment[0] += copysign(1,hori_dist)

def move_rope(head,tail,direction):
    match direction:
        case 'U':
            head[1] += 1
        case 'D':
            head[1] -= 1
        case 'R':
            head[0] += 1
        case 'L':
            head[0] -= 1
    for idx,segment in enumerate(tail):
        if idx == 0:
            target = head
        else:
            target = tail[idx-1]
        chase(target,segment)

with open('input.txt','r') as input:
    input_lines = input.read().splitlines()

tail_locations = set([(0,0)])
head = [0,0]
tail = [[0,0]]

longtail_locations = set([(0,0)])
longhead = [0,0]
longtail = [[0,0] for _ in range(9)]
for line in input_lines:
    direction,magnitude = line.split()
    magnitude = int(magnitude)
    for _ in range(magnitude):
        move_rope(head,tail,direction)
        tail_locations.add(tuple(tail[-1]))

        move_rope(longhead,longtail,direction)
        longtail_locations.add(tuple(longtail[-1]))

# Star 1
print(len(tail_locations))

# Star 2
print(len(longtail_locations))