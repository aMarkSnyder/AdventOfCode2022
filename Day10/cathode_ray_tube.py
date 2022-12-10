with open('input.txt','r') as input:
    input_lines = input.read().splitlines()

def pixel_art(sprite_center,clock_cycle):
    if abs(sprite_center - (clock_cycle-1)%40) <= 1:
        return '#'
    else:
        return '.'

start_of_cycle_values = [1]
crt_values = []
clock_cycle = 1
for line in input_lines:
    line = line.split()
    if len(line) == 1:
        crt_values.append(pixel_art(start_of_cycle_values[-1],clock_cycle))
        clock_cycle += 1
        start_of_cycle_values.append(start_of_cycle_values[-1])
    else:
        crt_values.append(pixel_art(start_of_cycle_values[-1],clock_cycle))
        clock_cycle += 1
        start_of_cycle_values.append(start_of_cycle_values[-1])

        crt_values.append(pixel_art(start_of_cycle_values[-1],clock_cycle))
        clock_cycle += 1
        start_of_cycle_values.append(start_of_cycle_values[-1]+int(line[1]))

# Star 1
print(sum([start_of_cycle_values[i]*(i+1) for i in range(19,220,40)]))

# Star 2
for row in range(6):
    print(''.join(crt_values[row*40:(row+1)*40]))