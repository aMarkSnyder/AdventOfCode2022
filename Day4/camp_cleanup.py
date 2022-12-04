# Star 1

def dominates(elf1,elf2):
    if int(elf1[0]) <= int(elf2[0]) and int(elf1[1]) >= int(elf2[1]):
        return True
    return False

with open('input.txt','r') as input:
    total_overlap = 0
    for pair in input:
        pair = pair.strip().split(',')
        elves = [elf.split('-') for elf in pair]
        if dominates(elves[0],elves[1]) or dominates(elves[1],elves[0]):
            total_overlap += 1

print(total_overlap)