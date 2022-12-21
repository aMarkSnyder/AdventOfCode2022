def binary_search(eval_string, low, high, goal):
    if high >= low:
        mid = (high + low) // 2
        current_val = eval_root(eval_string,mid)
        if current_val == goal:
            return mid
        # Line has negative slope, so if we're lower we need to move left
        elif current_val < goal:
            return binary_search(eval_string, low, mid - 1, goal)
        else:
            return binary_search(eval_string, mid + 1, high, goal)
    else:
        return -1

def eval_root(root_eval_string,humn):
    return eval(root_eval_string)

with open('input.txt','r',encoding='utf8') as input_file:
        lines = input_file.readlines()

# Star 1
monkeys = {}
for line in lines:
    name,expression = line.strip().split(': ')
    monkeys[name] = expression

while True:
    try:
        star1 = eval(monkeys['root'])
        break
    except:
        items = monkeys['root'].split()
        for idx,item in enumerate(items):
            left_parens = 1
            for char in item:
                if char == '(':
                    left_parens += 1
                else:
                    break
            right_parens = 1
            for char in item[::-1]:
                if char == ')':
                    right_parens += 1
                else:
                    break
            pure_item = item.strip('()')
            if pure_item in monkeys:
                items[idx] = '('*left_parens+monkeys[pure_item]+')'*right_parens
        monkeys['root'] = ' '.join(items)

print(star1)

# Star 2
monkeys = {}
for line in lines:
    name,expression = line.strip().split(': ')
    if name == 'root':
        expression = expression.replace('+','==')
    monkeys[name] = expression

humn = 1
while True:
    try:
        star2 = eval(monkeys['root'])
        break
    except:
        items = monkeys['root'].split()
        for idx,item in enumerate(items):
            left_parens = 1
            for char in item:
                if char == '(':
                    left_parens += 1
                else:
                    break
            right_parens = 1
            for char in item[::-1]:
                if char == ')':
                    right_parens += 1
                else:
                    break
            pure_item = item.strip('()')
            if pure_item in monkeys and pure_item != 'humn':
                items[idx] = '('*left_parens+monkeys[pure_item]+')'*right_parens
        monkeys['root'] = ' '.join(items)

goal = eval(monkeys['root'].split('==')[1])
print(binary_search(monkeys['root'].split('==')[0],0,1e15,goal))