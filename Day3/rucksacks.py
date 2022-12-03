# Star 1
with open('input.txt','r') as input:
    total_priority = 0
    for rucksack in input:
        contents = rucksack.strip()
        first_half = set(contents[:len(contents)//2])
        second_half = set(contents[len(contents)//2:])
        intersection = list(first_half.intersection(second_half))
        if ord(intersection[0]) >= 97:
            total_priority += ord(intersection[0]) - ord('a') + 1
        else:
            total_priority += ord(intersection[0]) - ord('A') + 27

print(total_priority)