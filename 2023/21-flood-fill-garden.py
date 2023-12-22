def add_to_coords_stk(grid_size, grid, coord):
    M, N = grid_size
    y, x = coord
    if 0 <= y < M and 0 <= x < N and grid[y][x] != "#":
        return True
    else:
        return False


def _fill_garden(grid):
    M, N = len(grid), len(grid)

    coords_stk = [(0, 0), (0, N - 1), (M - 1, 0), (M - 1, N - 1)]
    while coords_stk:
        y, x = coords_stk.pop()
        grid[y][x] = "#"
        neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        for n in neighbors:
            if add_to_coords_stk((M, N), grid, n):
                coords_stk.append(n)


if __name__ == "__main__":
    with open("../inputs/2023/21.txt") as f:
        grid = [list(line.strip()) for line in f.readlines()]

    _fill_garden(grid)
    unreachables = []
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile == ".":
                unreachables.append((i, j))
        print("".join(t for t in row))
    print(unreachables)


# this script was used to confirm that the input contained unreachable gardens
