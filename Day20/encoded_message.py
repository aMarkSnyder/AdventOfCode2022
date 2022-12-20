"""P"""

def mix(idx_map,nums):
    """p"""
    for old_idx,num in enumerate(nums):
        move(idx_map,old_idx,num)

def move(idx_map,old_idx,num):
    """p"""
    len_nums = len(idx_map)
    source = idx_map[old_idx]
    dest = (source + num) % (len_nums-1)

    # If move forward, everything from (old_position,new_position] moves back 1
    if dest - source > 0:
        for past_idx,new_idx in idx_map.items():
            if source < new_idx <= dest:
                idx_map[past_idx] -= 1
    # If move back, everything from [new_position,old_position) moves up 1
    elif dest - source < 0:
        for past_idx,new_idx in idx_map.items():
            if dest <= new_idx < source:
                idx_map[past_idx] += 1
    idx_map[old_idx] = dest

def get_new_nums(nums,idx_map):
    """p"""
    new_nums = [0 for _ in range(len(nums))]
    for old_idx,new_idx in idx_map.items():
        new_nums[new_idx] = nums[old_idx]
    return new_nums

def main():
    """p"""
    with open('input.txt','r',encoding='utf8') as input_file:
        nums = input_file.readlines()

    nums = [int(num) for num in nums]
    nums_len = len(nums)

    # Star 1
    idx_map = {idx:idx for idx in range(nums_len)}
    mix(idx_map,nums)
    new_nums = get_new_nums(nums,idx_map)
    zero_idx = new_nums.index(0)
    grove_coords = [new_nums[(zero_idx+offset)%nums_len] for offset in [1000,2000,3000]]
    print('1000th, 2000th, 3000th numbers after 0 are',grove_coords)
    print('their sum is',sum(grove_coords))

    # Star 2
    decryption_key = 811589153
    nums = [num*decryption_key for num in nums]
    idx_map = {idx:idx for idx in range(nums_len)}
    for _ in range(10):
        mix(idx_map,nums)
    new_nums = get_new_nums(nums,idx_map)
    zero_idx = new_nums.index(0)
    grove_coords = [new_nums[(zero_idx+offset)%nums_len] for offset in [1000,2000,3000]]
    print('1000th, 2000th, 3000th numbers after 0 are',grove_coords)
    print('their sum is',sum(grove_coords))

if __name__ == '__main__':
    main()
