with open('input.txt','r',encoding='utf8') as input_file:
    monkeys = input_file.readlines()
monkeys = [monkey.replace(':','=') for monkey in monkeys]

# Star 1
all_good = False
while not all_good:
    all_good = True
    for monkey in monkeys.copy():
        try:
            exec(monkey)
            monkeys.remove(monkey)
        except:
            all_good = False
            pass
print(root)