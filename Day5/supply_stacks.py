from collections import deque

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

with open('input.txt','r') as input:
    input_lines = input.readlines()
input_lines = input_lines[10:]

# Star 1
for line in input_lines:
    line = line.split()
    num_crates,source,dest = int(line[1]),int(line[3]),int(line[5])
    for _ in range(num_crates):
        stacks[dest].append(stacks[source].pop())

print(''.join([stack[-1] for stack in stacks[1:]]))