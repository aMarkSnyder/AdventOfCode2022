class Monkey():
    def __init__(self,items,operation,test_no,true_target,false_target) -> None:
        self.items = items
        self.operation = operation
        self.test_no = test_no
        self.true_target = true_target
        self.false_target = false_target
        self.inspected_items = 0
    
    def process_items(self,monkeys):
        targets = []
        for idx,item in enumerate(self.items):
            old = item
            new = eval(self.operation) // 3
            if new % self.test_no == 0:
                monkeys[self.true_target].items.append(new)
            else:
                monkeys[self.false_target].items.append(new)
            self.inspected_items += 1
        self.items = []

def initialize_monkeys(input_lines):
    monkeys = []
    idx = 0
    while idx < len(input_lines):
        items = [int(item) for item in input_lines[idx+1].split(':')[-1].split(',')]
        operation = input_lines[idx+2].split('=')[-1]
        test_no = int(input_lines[idx+3].split()[-1])
        true_target = int(input_lines[idx+4].split()[-1])
        false_target = int(input_lines[idx+5].split()[-1])
        monkeys.append(Monkey(items,operation,test_no,true_target,false_target))
        idx += 7
    return monkeys

with open('input.txt','r') as input:
    input_lines = input.read().splitlines()

monkeys = initialize_monkeys(input_lines)
for round in range(20):
    for monkey in monkeys:
        monkey.process_items(monkeys)
monkey_inspections = [monkey.inspected_items for monkey in monkeys]
monkey_inspections = sorted(monkey_inspections)
print(monkey_inspections[-2]*monkey_inspections[-1])