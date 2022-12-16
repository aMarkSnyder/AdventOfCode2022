import re
from collections import defaultdict
from itertools import permutations
import numpy as np

class Valve():
    def __init__(self,name,flow_rate,neighbors) -> None:
        self.name = name
        self.flow = flow_rate
        self.neighbors = neighbors

def BFS(valves, start_valve):
    queue = [start_valve]
    explored = set([start_valve])
    path_to = defaultdict(list)
    path_to[start_valve].append(start_valve)
    while queue:
        valve = queue.pop(0)
        neighbors = valves[valve].neighbors
        for neighbor in neighbors:
            if neighbor not in explored:
                explored.add(neighbor)
                path_to[neighbor] = path_to[valve] + [neighbor]
                queue.append(neighbor)
    return {valve:len(path_to[valve]) for valve in valves}

def generate_valid_routes(all_paths,curr_path,curr_valve,valuable_valves,visited_valves,distances,dest_valve,time,max_time):
    if time >= max_time:
        all_paths.add(tuple(curr_path))
        return
    if set([curr_valve]) == valuable_valves-visited_valves:
        all_paths.add(tuple(curr_path+[curr_valve]))
        return
    if curr_valve in visited_valves:
        return
    curr_path = curr_path + [curr_valve]
    visited_valves = visited_valves.union({curr_valve})
    for valve in valuable_valves-visited_valves:
        generate_valid_routes(all_paths,curr_path,valve,valuable_valves,visited_valves,distances,dest_valve,time+distances[curr_valve][valve],max_time)
    curr_path = curr_path[:-1]

def calculate_route_value(valves,distances,route,max_time,verbose=False):
    time = 0
    value = 0
    curr_valve = route[0]
    for stop in route[1:]:
        distance = distances[curr_valve][stop]
        time += distance
        if time >= max_time:
            break
        value += (max_time-time)*valves[stop].flow
        if verbose:
            print(f'opened {stop} at time {time}, so it will release {(max_time-time)*valves[stop].flow} total pressure')
        curr_valve = stop
    return value

with open('input.txt','r') as input_file:
    lines = input_file.readlines()

valves = {}
valuable_valves = set()
for line in lines:
    valve_names = re.findall('[A-Z][A-Z]', line)
    flow_rate = int(re.findall(r'\d+', line)[0])
    valve = Valve(valve_names[0],flow_rate,valve_names[1:])
    valves[valve.name] = valve
    if flow_rate:
        valuable_valves.add(valve.name)

distances = {}
for valve in valves:
    distances[valve] = BFS(valves,valve)

valuable_routes = set()
generate_valid_routes(valuable_routes,[],'AA',valuable_valves,set(),distances,valve,0,30)

max_value = 0
for route in valuable_routes:
    value = calculate_route_value(valves,distances,route,30)
    if value > max_value:
        max_value = value
print(max_value)