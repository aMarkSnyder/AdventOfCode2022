# Star 1
score_dict = {
    'X': {'A': 4, 'B': 1, 'C': 7},
    'Y': {'A': 8, 'B': 5, 'C': 2},
    'Z': {'A': 3, 'B': 9, 'C': 6}
}
with open('input.txt','r') as input:
    total_score = 0
    for game in input:
        opp,me = game.strip().split()
        total_score += score_dict[me][opp]

print(total_score)