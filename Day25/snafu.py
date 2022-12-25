def read_snafu(snafu):
	snafu_vals = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
	snafu = snafu[::-1]
	total = 0
	for idx,char in enumerate(snafu):
		total += snafu_vals[char] * 5**idx
	return total

def write_snafu(number):
	snafu_digits = ['0','1','2','=','-']
	snafu = []
	carry = False
	while number > 0 or carry:
		if carry:
			number += 1
			carry = False
		residue = number % 5
		if residue > 2:
			carry = True
		snafu.append(snafu_digits[residue])
		number = number // 5
	return snafu[::-1]

with open('input.txt','r',encoding='utf8') as input_file:
        snafus = input_file.readlines()
snafus = [[char for char in line.strip()] for line in snafus]

total = 0
for snafu in snafus:
	total += read_snafu(snafu)
print(''.join(write_snafu(total)))
