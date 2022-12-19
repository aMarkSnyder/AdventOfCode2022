import re
from tqdm import tqdm

class Sim():
    def __init__(self,blueprint,max_time,state=None) -> None:
        numbers = re.findall(r'\d+', blueprint)
        self.cost = {
            'ore': {'ore': int(numbers[1])},
            'clay': {'ore': int(numbers[2])},
            'obs': {'ore': int(numbers[3]), 'clay': int(numbers[4])},
            'geode': {'ore': int(numbers[5]), 'obs': int(numbers[6])}
        }
        self.max_time = max_time
        if state:
            self.load_state(state)
        else:
            self.stored = {
                'ore': 0,
                'clay': 0,
                'obs': 0,
                'geode': 0
            }
            self.production = {
                'ore': 1,
                'clay': 0,
                'obs': 0,
                'geode': 0
            }
            self.time = 0

    def get_state(self):
        return (self.stored.copy(),self.production.copy(),self.time)

    def load_state(self,state):
        self.stored, self.production, self.time = state

    def produce(self):
        for mat,gain in self.production.items():
            self.stored[mat] += gain

    def can_build(self,robot_type):
        if not robot_type:
            return True
        for mat,cost in self.cost[robot_type].items():
            if self.stored[mat] < cost:
                return False
        return True

    def can_ever_build(self,robot_type):
        if not robot_type:
            return True
        for mat in self.cost[robot_type]:
            if self.production[mat] == 0:
                return False
        return True

    def build(self,robot_type):
        if robot_type == 'end':
            return self.fast_forward()
        if not self.can_ever_build(robot_type):
            return -1
        start_time = self.time
        while not self.can_build(robot_type) and self.time < self.max_time:
            self.produce()
            self.time += 1
        if self.time > self.max_time:
            return -1
        self.produce()
        self.time += 1
        if robot_type:
            for mat,cost in self.cost[robot_type].items():
                self.stored[mat] -= cost
            self.production[robot_type] += 1
        return self.time - start_time

    def time_to_build(self,robot_type):
        state = self.get_state()
        time = self.build(robot_type)
        self.load_state(state)
        return time

    def fast_forward(self):
        start_time = self.time
        self.time = self.max_time
        time_diff = self.time - start_time
        for mat,gain in self.production.items():
            self.stored[mat] += time_diff*gain
        return time_diff


# def generate_valid_routes(all_paths,curr_path,curr_valve,valuable_valves,visited_valves,distances,time,max_time):
#     if time >= max_time:
#         all_paths.add(tuple(curr_path))
#         return
#     if set([curr_valve]) == valuable_valves-visited_valves:
#         all_paths.add(tuple(curr_path+[curr_valve]))
#         return
#     if curr_valve in visited_valves:
#         return
#     curr_path = curr_path + [curr_valve]
#     visited_valves = visited_valves.union({curr_valve})
#     for valve in valuable_valves-visited_valves:
#         generate_valid_routes(all_paths,curr_path,valve,valuable_valves,visited_valves,distances,time+distances[curr_valve][valve],max_time)

def generate_valid_routes(all_paths,curr_path,curr_action,blueprint,max_time,state):
    if state[-1] == max_time:
        all_paths.add(state[0]['geode'])
        return
    sim = Sim(blueprint,max_time,state)
    if sim.build(curr_action) == -1:
        #print(curr_action,'will take too long after',curr_path)
        return
    curr_path = curr_path + [curr_action]
    valuable_actions = []
    if sim.production['ore'] < 6:
        valuable_actions.append('ore')
    if sim.production['clay'] < 10:
        valuable_actions.append('clay')
    if sim.can_ever_build('obs'):
        valuable_actions.append('obs')
    if sim.can_ever_build('geode'):
        valuable_actions.append('geode')
    if sim.production['geode'] > 0:
        valuable_actions.append('end')
    if sim.can_build('geode'):
        valuable_actions = ['geode']
    for action in valuable_actions:
        generate_valid_routes(all_paths,curr_path,action,blueprint,max_time,sim.get_state())

with open('input.txt','r') as input_file:
    blueprints = input_file.readlines()

max_geodes = []
for blueprint in tqdm(blueprints):
    base_sim = Sim(blueprint,24)
    geodes = set()
    generate_valid_routes(geodes,[],None,blueprint,24,base_sim.get_state())
    max_geodes.append(max(geodes))
print(max_geodes)
print(sum([idx*count for idx,count in enumerate(max_geodes,start=1)]))