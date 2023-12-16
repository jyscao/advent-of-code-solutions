def get_light_vec(light_vec, tile):
    if tile == ".":
        return [light_vec]

    lx, ly = light_vec
    if bool(lx) and not bool(ly):
        return {
            '\\': [(0, lx)],
            '/':  [(0, -lx)],
            '|':  [(0, 1), (0, -1)],
            '-':  [light_vec],
        }[tile]
    elif not bool(lx) and bool(ly):
        return {
            '\\': [(ly, 0)],
            '/':  [(-ly, 0)],
            '|':  [light_vec],
            '-':  [(1, 0), (-1, 0)],
        }[tile]
    else:
        raise Exception("this should never be reached")


def get_energized_tiles(space, init_pos_dir_vec):
    M, N = len(space), len(space[0])
    light_tile_set = set()

    light_heads = [init_pos_dir_vec]
    while light_heads:
        x, y, lx, ly = pos_dir_vec = light_heads.pop()

        if pos_dir_vec in light_tile_set:
            continue
        else:
            light_tile_set.add(pos_dir_vec)

        for lx, ly in get_light_vec((lx, ly), space[x][y]):
            if 0 <= x + lx < N and 0 <= y + ly < M:
                light_heads.append((x + lx, y + ly, lx, ly,))

    return len({(x, y) for x, y, _, _ in light_tile_set})



def find_max_energization(space):
    N = len(space) - 1
    max_tiles = 0

    corners = [
        (0, 0, 1, 0), (0, 0, 0, 1), (N, 0, -1, 0), (N, 0, 0, 1),
        (0, N, 1, 0), (0, N, 0, -1), (N, N, -1, 0), (N, N, 0, -1),
    ]
    top   = [(x, 0, 0, 1) for x in range(1, N)]
    bot   = [(x, N, 0, -1) for x in range(1, N)]
    left  = [(0, y, 1, 0) for y in range(1, N)]
    right = [(N, y, -1, 0) for y in range(1, N)]

    for init_conds in corners + top + bot + left + right:
        energized_tiles = get_energized_tiles(space, init_conds)
        max_tiles = max(max_tiles, energized_tiles)

    return max_tiles



if __name__ == "__main__":
    with open("../inputs/2023/16.txt") as f:
        data = [line.strip() for line in f.readlines()]

    test_data = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
    """
    # data = test_data.strip().splitlines()

    space = list(zip(*data))

    print(get_energized_tiles(space, (0, 0, 1, 0)))     # part 1
    print(find_max_energization(space))                 # part 2
