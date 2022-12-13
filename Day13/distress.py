def is_correct_order(left,right):
    if isinstance(left,int) and isinstance(right,int):
        if left < right:
            return 1
        if left > right:
            return -1
        return 0
    elif isinstance(left,int) and isinstance(right,list):
        return is_correct_order([left],right)
    elif isinstance(left,list) and isinstance(right,int):
        return is_correct_order(left,[right])
    else:
        for left_item,right_item in zip(left,right):
            if res := is_correct_order(left_item,right_item):
                return res
        return is_correct_order(len(left),len(right))
            

with open('input.txt','r') as input_file:
    pairs = input_file.read().split('\n\n')

pairs = [pair.split('\n') for pair in pairs]
correct_order = []
for idx,pair in enumerate(pairs):
    left,right = [eval(line) for line in pair if line != '']
    if is_correct_order(left,right) == 1:
        correct_order.append(idx+1)

# Star 1
print(sum(correct_order))
