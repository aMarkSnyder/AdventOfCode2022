# Star 1
def dominates(elf1,elf2):
    elf1 = set(range(int(elf1[0]),int(elf1[1])+1))
    elf2 = set(range(int(elf2[0]),int(elf2[1])+1))
    return len(elf1.union(elf2)) == len(elf1) or len(elf1.union(elf2)) == len(elf2)

# Star 2
def overlaps(elf1,elf2):
    elf1 = set(range(int(elf1[0]),int(elf1[1])+1))
    elf2 = set(range(int(elf2[0]),int(elf2[1])+1))
    return len(elf1.intersection(elf2))

with open('input.txt','r') as input:
    total_domination = 0
    total_overlap = 0
    for pair in input:
        pair = pair.strip().split(',')
        elves = [elf.split('-') for elf in pair]
        if dominates(elves[0],elves[1]):
            total_domination += 1
            total_overlap += 1
        elif overlaps(elves[0],elves[1]):
            total_overlap += 1

print(total_domination)
print(total_overlap)