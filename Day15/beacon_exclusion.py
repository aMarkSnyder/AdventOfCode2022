import re
from collections import defaultdict
import numpy as np

def manhattan(point1,point2):
    return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])

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

excluded = 0
y = 2000000
for x in range(far_left,far_right+1):
    for sensor,(beacon,distance) in sensors.items():
        if manhattan(sensor,(x,y)) <= distance and (x,y) != beacon:
            excluded += 1
            break
print(excluded)
