from itertools import combinations

def expand_space(space):
    n_space = []
    for row in space:
        if all(s == "." for s in row):
            n_space += [row, row]
        else:
            n_space.append(row)

    new_space = []
    for col in zip(*n_space):
        if all(s == "." for s in col):
            new_space += [col, col]
        else:
            new_space.append(col)

    return ["".join(i) for i in zip(*new_space)]


def expand_space2(space):
    n_space, R = [], []
    for i, row in enumerate(space):
        if all(s == "." for s in row):
            n_space.append("+" * len(row))
            R.append(i)
        else:
            n_space.append(row)

    new_space, C = [], []
    for j, col in enumerate(zip(*n_space)):
        if all(s in (".", "+") for s in col):
            new_space.append("+" * len(col))
            C.append(j)
        else:
            new_space.append(col)

    return ["".join(i) for i in zip(*new_space)], (R, C)


def get_galaxies(space):
    galaxies = []
    for i, row in enumerate(space):
        for j, pos in enumerate(row):
            if pos == "#":
                galaxies.append((i, j))
    return galaxies

def calc_tot_dist(galaxies):
    res = 0
    for g1, g2 in combinations(galaxies, 2):
        x1, y1 = g1
        x2, y2 = g2
        res += abs(x1 - x2) + abs(y1 - y2)
    return res


def calc_tot_dist2(expansions, galaxies):
    expansion_factor = 1_000_000
    res = 0
    X, Y = expansions
    for g1, g2 in combinations(galaxies, 2):
        x1, y1 = g1
        x2, y2 = g2
        if y1 > y2:
            y1, y2 = y2, y1
        assert x1 <= x2 and y1 <= y2

        x_range, y_range = range(x1, x2), range(y1, y2)
        x_extras = [1 for x in X if x in x_range]
        y_extras = [1 for y in Y if y in y_range]
        Nx, Ny = len(x_extras), len(y_extras)
        res += len(x_range) + len(y_range) + expansion_factor * (sum(x_extras) + sum(y_extras)) - Nx - Ny
    return res


if __name__ == "__main__":
    with open("../inputs/2023/11.txt") as f:
        data = [line.strip() for line in f.readlines()]

    expanded_space1 = expand_space(data)
    galaxies1 = get_galaxies(expanded_space1)
    print(calc_tot_dist(galaxies1))

    expanded_space2, expansions = expand_space2(data)
    galaxies2 = get_galaxies(expanded_space2)
    print(calc_tot_dist2(expansions, galaxies2))





# NOTE: a cleaner implementation found on Reddit:
# https://www.reddit.com/r/adventofcode/comments/18fmrjk/2023_day_11_solutions/kcvd4io/
# https://github.com/fuglede/adventofcode/blob/master/2023/day11/solutions.py

# from itertools import combinations
#
# with open("../inputs/2023/11.txt") as f:
#     ls = f.read().strip().split("\n")
#
# empty = {j for j in range(len(ls[0])) if all(ls[i][j] != "#" for i in range(len(ls)))}
# galaxies = {(i, j) for i, l in enumerate(ls) for j, x in enumerate(l) if x == "#"}
# pairs = list(combinations(galaxies, 2))
#
#
# def dist(x1, x2, y1, y2, scale):
#     cols = set(range(x2, y2, 1 if y2 > x2 else -1))
#     return abs(x1 - y1) + abs(x2 - y2) + len(empty & cols) * scale
#
#
# # Part 1
# print(sum(dist(*x, *y, 1) for x, y in pairs))
#
# # Part 2
# print(sum(dist(*x, *y, 999_999) for x, y in pairs))
