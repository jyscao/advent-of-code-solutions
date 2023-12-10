def get_pipe_dirs(tile):
    return {
        "|" : ("N", "S"),
        "-" : ("W", "E"),
        "L" : ("N", "E"),
        "J" : ("N", "W"),
        "7" : ("S", "W"),
        "F" : ("S", "E"),
        "." : (),
        "S" : ("N", "W"),
    }[tile]


def dir_2_coord(coord, dir):
    i, j = coord
    return {
        "N": (i - 1, j),
        "S": (i + 1, j),
        "W": (i, j - 1),
        "E": (i, j + 1),
    }[dir]


def convert_src_dir(src_dir):
    return {
        "N": "S",
        "S": "N",
        "W": "E",
        "E": "W",
    }[src_dir]


def advance_to_next(maze_mat, coord, src_dir):
    i, j = coord
    tile = maze_mat[i][j]
    adv_dir = [dir for dir in get_pipe_dirs(tile) if dir != convert_src_dir(src_dir)][0]
    return dir_2_coord(coord, adv_dir), adv_dir


def find_start(maze_mat):
    for i, row in enumerate(maze_mat):
        for j, tile in enumerate(row):
            if tile == "S":
                return i, j


def follow_pipe(maze_mat):
    steps = 0
    i, j = nx_coord = find_start(maze_mat)
    tile = maze_mat[i][j]
    nx_dir = "E"
    # nx_dir = "N"
    while tile != "S" or steps == 0:
        nx_coord, nx_dir = advance_to_next(maze_mat, nx_coord, nx_dir)
        i, j = nx_coord
        tile = maze_mat[i][j]
        steps += 1

    return steps


def double_tile(tile):
    return {
        "|" : ("|.", "|."),
        "-" : ("--", ".."),
        "L" : ("L-", ".."),
        "J" : ("J.", ".."),
        "7" : ("7.", "|."),
        "F" : ("F-", "|."),
        "." : ("..", ".."),
        "S" : ("S.", ".."),
    }[tile]


def double_maze(maze_mat):
    new_maze = []
    for row in maze_mat:
        r1, r2 = "", ""
        for tile in row:
            a, b = double_tile(tile)
            r1 += a
            r2 += b
        new_maze += [r1, r2]
    return new_maze


def map_pipe(maze_mat):
    i, j = nx_coord = find_start(maze_mat)
    main_pipe = {nx_coord}
    tile = maze_mat[i][j]
    # nx_dir = "E"
    nx_dir = "N"
    # nx_dir = "W"
    while tile != "S" or len(main_pipe) == 1:
        nx_coord, nx_dir = advance_to_next(maze_mat, nx_coord, nx_dir)
        main_pipe.add(nx_coord)
        i, j = nx_coord
        tile = maze_mat[i][j]
    return main_pipe


def add_to_coords_stk(mat_size, coord, fill_status):
    M, N = mat_size
    i, j = coord
    if 0 <= i < M and 0 <= j < N and fill_status[i][j] is False:
        return True
    else:
        return False


def get_original_fill(maze_mat, pipe_map):
    M, N = len(maze_mat), len(maze_mat[0])
    fill_status = [[False] * N for _ in range(M)]
    for i, row in enumerate(fill_status):
        for j, _ in enumerate(row):
            if (i, j) in pipe_map:
                fill_status[i][j] = True
    return fill_status


def flood_fill(maze_mat, pipe_map):
    M, N = len(maze_mat), len(maze_mat[0])

    fill_status = [[False] * N for _ in range(M)]
    for i, row in enumerate(fill_status):
        for j, _ in enumerate(row):
            if (i, j) in pipe_map:
                fill_status[i][j] = True

    coords_stk = [(0, 0), (0, N - 1), (M - 1, 0), (M - 1, N - 1)]
    while coords_stk:
        i, j = coords_stk.pop()
        fill_status[i][j] = True
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        for n in neighbors:
            if add_to_coords_stk((M, N), n, fill_status):
                coords_stk.append(n)

    return sum(sum(t for t in row[::2]) for row in fill_status[::2])



def get_total_area(maze):
    return len(maze) * len(maze[0])



if __name__ == "__main__":
    with open("../inputs/2023/10.txt") as f:
        maze_mat = [line.strip() for line in f.readlines()]

    print(follow_pipe(maze_mat))    # part 1 answer

    # NOTE: idea on how to solve part 2 was taken from: https://www.reddit.com/r/adventofcode/comments/18evyu9/2023_day_10_solutions/

    maze_mat = double_maze(maze_mat)
    pipe_map = map_pipe(maze_mat)

    tot_area_double_res = get_total_area(maze_mat)
    non_area_counted = flood_fill(maze_mat, pipe_map)
    print(tot_area_double_res / 4 - non_area_counted)   # part 2 answer
