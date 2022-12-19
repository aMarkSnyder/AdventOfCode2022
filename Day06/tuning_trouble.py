with open('input.txt','r') as input:
    input_line = input.readlines()[0]

# Star 1
for i in range(4,len(input_line)):
    if len(set(input_line[i-4:i])) == 4:
        print(i)
        break
# Star 2
for i in range(4,len(input_line)):
    if len(set(input_line[i-14:i])) == 14:
        print(i)
        break