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
    # See: https://www.reddit.com/r/adventofcode/comments/18nevo3/2023_day_21_solutions/?sort=top
    #
    # A key observation which makes the answer solvable as a quadratic is that:
    # "the input was crafted in such a way that the start point was in the
    # center of the grid, the row and column of the start point were completely
    # empty, and the diagonal lines connecting the midpoints of each edge were
    # also empty"
    #
    # therefore, 'S' is in the center of the garden, 131 is the side length of
    # square garden and 65 is the distance from 'S' to either the mid-point of
    # the top, bottom, left or right sides
    #
    # The quadratic coefficients A & B were obtained by solving for f(0), f(1) & f(2);
    # where x0 = 65, x1 = 65 + 131, x2 = 65 + 131*2
    #
    # the original grid was extended into 5x5 repeats to obtain the correct reachables
    # empirically calculating using the functions from part 1, we have:
    start = find_start(grid)
    s0, s1, s2 = 65, 65 + 131, 65 + 131 * 2
    sizes = [len(build_reachables_map(grid, s2, start)[s]) for s in (s0, s1, s2)]
    print(sizes)    # [3832, 33967, 94056]

    # with the above f(x)'s, a quadratic was fitted using Wolfram Alpha: https://www.wolframalpha.com/input?i=quadratic+fit+calculator&assumption=%7B%22F%22%2C+%22QuadraticFitCalculator%22%2C+%22data3x%22%7D+-%3E%22%7B0%2C+1%2C+2%7D%22&assumption=%7B%22F%22%2C+%22QuadraticFitCalculator%22%2C+%22data3y%22%7D+-%3E%22%7B3832%2C+33967%2C+94056%7D%22
    # with the equation being: f(x) = 14977x^2 + 15158x + B3832
    #
    # b/c n_steps = 131x + 65, so for n_steps = 26501365, x = 202300
    # and finally, solve for f(202300):
    def solve(n_steps):
        x = (n_steps - 65) // 131
        A = 14977
        B = 15158
        return A * x * x + B * x + 3832
    print(solve(26501365))  # 612941134797232
