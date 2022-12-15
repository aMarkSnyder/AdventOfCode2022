import re
from collections import defaultdict
import numpy as np

def manhattan(point1,point2):
    return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])

def get_edge_points(sensor,distance):
    edge_points = set()
    left,right = sensor[0]-distance-1,sensor[0]+distance+1
    for offset in range(distance+2):
        edge_points.add((left+offset,sensor[1]+offset))
        edge_points.add((left+offset,sensor[1]-offset))
        edge_points.add((right-offset,sensor[1]+offset))
        edge_points.add((right-offset,sensor[1]-offset))
    return edge_points

with open('input.txt','r') as input_file:
    lines = input_file.readlines()

sensors = {}
beacons = defaultdict(list)
far_left = np.inf
far_right = -np.inf
for line in lines:
    sensorx,sensory,beaconx,beacony = re.findall(r'\d+', line)
    sensorx,sensory,beaconx,beacony = int(sensorx),int(sensory),int(beaconx),int(beacony)
    sensor,beacon = (sensorx,sensory),(beaconx,beacony)
    distance = manhattan(sensor,beacon)
    sensors[sensor] = [beacon,distance]
    beacons[beacon].append([sensor,distance])
    if sensor[0]-distance < far_left:
        far_left = sensor[0]-distance
    if sensor[0]+distance > far_right:
        far_right = sensor[0]+distance

# # Star 1
excluded = 0
y = 2000000
for x in range(far_left,far_right+1):
    for sensor,(beacon,distance) in sensors.items():
        if manhattan(sensor,(x,y)) <= distance and (x,y) != beacon:
            excluded += 1
            break
print(excluded)

# Star 2
edge_points = []
candidates = set()
for idx,sensor in enumerate(sensors):
    for idx2,sensor2 in enumerate(sensors):
        if idx == idx2:
            continue
        if manhattan(sensor,sensor2) == sensors[sensor][1]+sensors[sensor2][1]+2:
            edge_pts = get_edge_points(sensor,sensors[sensor][1])
            possibles = edge_pts.intersection(get_edge_points(sensor2,sensors[sensor2][1]))
            for point in possibles:
                if 0 <= point[0] <= 4000000 and 0 <= point[1] <= 4000000:
                    candidates.add(point)

for candidate in candidates:
    allowed = True
    for sensor,(_,distance) in sensors.items():
        if manhattan(sensor,(candidate)) <= distance:
            allowed = False
            break
    if allowed:
        print(candidate[0]*4000000+candidate[1])
