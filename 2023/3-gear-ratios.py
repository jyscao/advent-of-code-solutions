import re


def get_data():
    with open("../inputs/2023/3.txt") as f:
        raw_data = [line.strip() for line in f.readlines()]

    n = len(raw_data[0])
    pad_data = ["." * n] + raw_data + ["." * n]
    data = []
    for row in pad_data:
        data.append(f".{row}.")

    return data


def get_num_pos_pairs(data):
    num_sep_re = re.compile(r"[-.@&*=+$%#/]")
    num_pos_pairs = []
    for i, row in enumerate(data):
        x, nums = 0, [n for n in num_sep_re.split(row) if n]
        nn = len(nums)
        for j, _ in enumerate(row):
            if x < nn and row.startswith(nums[x], j) and not row[j-1].isdigit():
                num_pos_pairs.append((nums[x], (i, j)))
                x += 1
    return num_pos_pairs


def gear1(data):
    res = 0
    for np_tup in get_num_pos_pairs(data):
        if num_near_symbol(data, np_tup):
            res += int(np_tup[0])
    return res


def num_near_symbol(data, np_tup):
    num, (row, start) = np_tup
    nl = len(num)
    num_pos = [(row, p) for p in range(start, start + nl)]
    pos_to_check = [(i, j) for i in range(row - 1, row + 2) for j in range(start - 1, start + nl + 1) if (i, j) not in num_pos]
    res = any(data[x][y] in "@&*=+$%-#/" for x, y in pos_to_check)
    return res


def gear2(data):
    gear_candidates = get_gear_candidates(data)
    gears = {}
    for num, gear_coord in gear_candidates:
        if gear_coord in gears:
            gears[gear_coord].append(num)
        else:
            gears[gear_coord] = [num]
    gears = {coord: parts for coord, parts in gears.items() if len(parts) == 2}
    # assert all(len(parts) == 2 for parts in gears.values())

    res = 0
    for (g1, g2) in gears.values():
        res += int(g1) * int(g2)

    return res
    


def get_adjacent_coords(np_tup):
    num, (row, start) = np_tup
    nl = len(num)
    num_pos = [(row, p) for p in range(start, start + nl)]
    return [(i, j) for i in range(row - 1, row + 2) for j in range(start - 1, start + nl + 1) if (i, j) not in num_pos]


def get_gear_candidates(data):
    num_pos_pairs = get_num_pos_pairs(data)
    gear_candidates = []
    for np_tup in num_pos_pairs:
        for i, j in get_adjacent_coords(np_tup):
            if data[i][j] == "*":
                gear_candidates.append((np_tup[0], (i, j)))
    return gear_candidates



if __name__ == "__main__":
    data = get_data()
    ans1 = gear1(data)  # wrong: 533776; correct: 533784
    print(ans1)
    ans2 = gear2(data)
    print(ans2)
