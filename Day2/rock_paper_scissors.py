# Star 1
score_dict1 = {
    'X': {'A': 4, 'B': 1, 'C': 7},
    'Y': {'A': 8, 'B': 5, 'C': 2},
    'Z': {'A': 3, 'B': 9, 'C': 6}
}
# Star 2
score_dict2 = {
    'A': {'X': 3, 'Y': 4, 'Z': 8},
    'B': {'X': 1, 'Y': 5, 'Z': 9},
    'C': {'X': 2, 'Y': 6, 'Z': 7}
}
with open('input.txt','r') as input:
    total_score1, total_score2 = 0, 0
    for game in input:
        opp,me = game.strip().split()
        total_score1 += score_dict1[me][opp]
        total_score2 += score_dict2[opp][me]

print(total_score1)
print(total_score2)