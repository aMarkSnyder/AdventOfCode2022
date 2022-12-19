import re
from math import prod
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
        if not self.can_ever_build(robot_type):
            return -1
        start_time = self.time
        while not self.can_build(robot_type) and self.time < self.max_time:
            self.produce()
            self.time += 1
        if self.time == self.max_time:
            return self.time - start_time
        self.produce()
        self.time += 1
        if robot_type:
            for mat,cost in self.cost[robot_type].items():
                self.stored[mat] -= cost
            self.production[robot_type] += 1
        return self.time - start_time

def count_geodes(geode_counts,next_bot,blueprint,max_time,state):
    if state[-1] == max_time:
        geode_counts.add(state[0]['geode'])
        return
    sim = Sim(blueprint,max_time,state)
    if sim.build(next_bot) == -1:
        return
    valuable_bots = []
    if sim.production['ore'] < 4:
        valuable_bots.append('ore')
    if sim.production['clay'] < 10:
        valuable_bots.append('clay')
    if sim.can_ever_build('obs'):
        valuable_bots.append('obs')
    if sim.can_ever_build('geode'):
        valuable_bots.append('geode')
    if sim.can_build('obs'):
        valuable_bots = ['clay','obs']
    if sim.can_build('geode'):
        valuable_bots = ['geode']
    for bot in valuable_bots:
        count_geodes(geode_counts,bot,blueprint,max_time,sim.get_state())

with open('input.txt','r') as input_file:
    blueprints = input_file.readlines()

# Star 1
max_geodes = []
for blueprint in tqdm(blueprints):
    base_sim = Sim(blueprint,24)
    geodes = set()
    count_geodes(geodes,None,blueprint,24,base_sim.get_state())
    max_geodes.append(max(geodes))
print(max_geodes)
print(sum([idx*count for idx,count in enumerate(max_geodes,start=1)]))

# Star 2
max_geodes = []
for blueprint in tqdm(blueprints[:3]):
    base_sim = Sim(blueprint,32)
    geodes = set()
    count_geodes(geodes,None,blueprint,32,base_sim.get_state())
    max_geodes.append(max(geodes))
print(max_geodes)
print(prod(max_geodes))