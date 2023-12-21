def get_next_reachables(grid, pos):
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
            r_map[i].update(get_next_reachables(grid, pos))

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
    n_steps = 10
    # n_steps = 26_501_365
