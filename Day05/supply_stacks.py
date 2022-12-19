from collections import deque

with open('input.txt','r') as input:
    input_lines = input.readlines()
input_lines = input_lines[10:]

# Star 1
stacks = [[None],
          deque(['G','T','R','W']),
          deque(['G','C','H','P','M','S','V','W']),
          deque(['C','L','T','S','G','M']),
          deque(['J','H','D','M','W','R','F']),
          deque(['P','Q','L','H','S','W','F','J']),
          deque(['P','J','D','N','F','M','S']),
          deque(['Z','B','D','F','G','C','S','J']),
          deque(['R','T','B']),
          deque(['H','N','W','L','C'])]
          
for line in input_lines:
    line = line.split()
    num_crates,source,dest = int(line[1]),int(line[3]),int(line[5])
    for _ in range(num_crates):
        stacks[dest].append(stacks[source].pop())

print(''.join([stack[-1] for stack in stacks[1:]]))

# Star 2
stacks = [[None],
          ['G','T','R','W'],
          ['G','C','H','P','M','S','V','W'],
          ['C','L','T','S','G','M'],
          ['J','H','D','M','W','R','F'],
          ['P','Q','L','H','S','W','F','J'],
          ['P','J','D','N','F','M','S'],
          ['Z','B','D','F','G','C','S','J'],
          ['R','T','B'],
          ['H','N','W','L','C']]

for line in input_lines:
    line = line.split()
    num_crates,source,dest = int(line[1]),int(line[3]),int(line[5])
    stacks[dest].extend(stacks[source][-num_crates:])
    stacks[source] = stacks[source][:-num_crates]

print(''.join([stack[-1] for stack in stacks[1:]]))
