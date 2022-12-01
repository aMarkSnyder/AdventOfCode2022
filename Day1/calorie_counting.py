# Star 1
elves = []
with open('input.txt','r') as input:
    elf = []
    for line in input:
        if line == '\n':
            elves.append(elf)
            elf = []
        else:
            elf.append(int(line))

calorie_totals = [sum(elf) for elf in elves]

print(max(calorie_totals))