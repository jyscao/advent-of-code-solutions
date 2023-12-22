def get_reachable_neighbors(grid, pos):
    M, N = len(grid), len(grid[0])
    y, x = pos
    return set((i, j) for i, j in 
        ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))
        if 0 <= i < M and 0 <= j < N and grid[i][j] != "#")


def build_reachables_map(grid, n_steps, start_pos):
    r_map = {i: set() for i in range(1, n_steps + 1)}
    r_map[0] = {start_pos}
    for i in range(1, n_steps + 1):
        for pos in r_map[i - 1]:
            r_map[i].update(get_reachable_neighbors(grid, pos))
    return r_map

def find_start(grid):
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile == "S":
                return i, j


# def get_n_available_plots(grid):
#     M, N = len(grid), len(grid[0])
#     n_rocks = sum(row.count("#") for row in grid)
#     return M * N - n_rocks
#
#
# def get_corner_and_edge_plots(grid):
#     m, n = len(grid) - 1, len(grid[0]) - 1
#     corners = [(0, 0), (0, n), (m, 0), (m, n)]
#     edges_hor = [(i , j) for i in (0, m) for j in range(1, n)]
#     edges_ver = [(i , j) for i in range(1, m) for j in (0, n)]
#     return corners, edges_hor + edges_ver
#
#
# def get_next_reachables_from_prev(grid, prev_reachables):
#     next_reachables = set()
#     for pos in prev_reachables:
#         next_reachables.update(get_reachable_neighbors(grid, pos))
#     return next_reachables
#
#
# def get_min_steps_and_total_available(grid, start_pos):
#     def reached_max(even_tup, odd_tup):
#         e_p, e_c = map(len, even_tup)
#         o_p, o_c   = map(len, odd_tup)
#         if e_p == e_c and o_p == o_c:
#             return True, (e_c, o_c)
#         else:
#             return False,(e_c, o_c)
#
#     even_prev, even_curr = set(), {start_pos}
#     odd_prev, odd_curr   = set(), get_next_reachables_from_prev(grid, even_curr)
#     steps = 1
#     while True:
#         max_reached, (even_tot, odd_tot) = reached_max((even_prev, even_curr), (odd_prev, odd_curr))
#         if max_reached:
#             return (steps - 3, even_tot), (steps - 2, odd_tot)
#         else:
#             even_prev, even_curr = even_curr, get_next_reachables_from_prev(grid, odd_curr)
#             steps += 1
#             
#         max_reached, (even_tot, odd_tot) = reached_max((even_prev, even_curr), (odd_prev, odd_curr))
#         if max_reached:
#             return (steps - 2, even_tot), (steps - 3, odd_tot)
#         else:
#             odd_prev, odd_curr = odd_curr, get_next_reachables_from_prev(grid, even_curr)
#             steps += 1



if __name__ == "__main__":
    with open("../inputs/2023/21.txt") as f:
        grid = [line.strip() for line in f.readlines()]

    test_data = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
    """
    # grid = [line.strip() for line in test_data.strip().splitlines()]

    # part 1
    start = find_start(grid)
    n_steps = 64
    reachables_map = build_reachables_map(grid, n_steps, start)
    print(len(reachables_map[n_steps]))


    # part 2
    # see: https://www.reddit.com/r/adventofcode/comments/18nevo3/2023_day_21_solutions/?sort=top
    # 
    # Wolfram Alpha solve: https://www.wolframalpha.com/input?i=quadratic+fit+calculator&assumption=%7B%22F%22%2C+%22QuadraticFitCalculator%22%2C+%22data3x%22%7D+-%3E%22%7B0%2C+1%2C+2%7D%22&assumption=%7B%22F%22%2C+%22QuadraticFitCalculator%22%2C+%22data3y%22%7D+-%3E%22%7B3832%2C+33967%2C+94056%7D%22
    # the equation is: f(x) = 14977x^2 + 15158x + 3832, where 131x + 65 = N_steps
    #
    # the quadratic coefficients A & B were obtained by solving for f(0), f(1) & f(2); the original grid was extended into a 5x5 repeats
    # the empirically solving using the functions from part 1, like so:
    start = find_start(grid)
    s0, s1, s2 = 65, 65 + 131, 65 + 131 * 2
    sizes = [len(build_reachables_map(grid, s, start)[s]) for s in (s0, s1, s2)]
    print(sizes)
