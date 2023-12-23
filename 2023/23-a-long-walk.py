import networkx as nx


def get_start_and_end(grid):
    m, n = len(grid) - 1, len(grid[0]) - 1
    return (0, 1), (m, n - 1)


def get_nodes(grid):
    m, n = len(grid) - 1, len(grid[0]) - 1

    def is_branching_node(pos):
        y, x = pos
        neighbors = ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1),)
        n_tiles = set(grid[i][j] for i, j in neighbors if 0<=i<=m and 0<=j<=n)
        return "v" in n_tiles and ">" in n_tiles

    branching_nodes = set()
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile == "#":
                continue
            elif tile == "." and is_branching_node((i, j)):
                branching_nodes.add((i, j))

    return branching_nodes


def follow_path_get_steps(pos, dir, nodes, grid):
    m, n = len(grid) - 1, len(grid[0]) - 1
    _, end = get_start_and_end(grid)

    def get_new_dir(pos, dir):
        y, x = pos
        src_dir = tuple(-1 * c for c in dir)
        orth_dirs = (d for d in ((-1, 0), (1, 0), (0, -1), (0, 1),) if d != src_dir)
        nd_tup = [(grid[y + vy][x + vx], (vy, vx),) for vy, vx in orth_dirs if 0<=y+vy<=m and 0<=x+vx<=n]
        neighbor_tiles, neighbor_dirs = zip(*nd_tup)
        if "." in neighbor_tiles and neighbor_tiles.count(".") == 1:
            return [d for tile, d in nd_tup if tile == "."][0]
        elif "v" in neighbor_tiles:
            return 1, 0
        elif ">" in neighbor_tiles:
            return 0, 1
        else:
            raise Exception("this should never be reached!")

    steps = 0
    y, x = pos
    vy, vx = dir
    non_self_nodes = nodes.difference({pos})
    while pos not in non_self_nodes:
        try:
            y_t, x_t = y + vy, x + vx
            assert grid[y_t][x_t] in {".", "v", ">",}
            y, x = pos = y_t, x_t
        except AssertionError:
            vy, vx = dir = get_new_dir(pos, dir)
            y += vy
            x += vx
            pos = (y, x)
        steps += 1

        if pos == end:
            break

    return pos, steps


def get_paths_lengths(grid):
    nodes = get_nodes(grid)
    start, _ = get_start_and_end(grid)

    edge_map = {n: {} for n in nodes}
    edge_map[start] = {}

    node_stk = [(start, (1, 0),)]
    while node_stk:
        src, dir = node_stk.pop()
        dest, n_steps = follow_path_get_steps(src, dir, nodes, grid)
        edge_map[src][dest] = n_steps

        if dest in nodes and not bool(edge_map[dest]):
            node_stk.append((dest, (1, 0),))
            node_stk.append((dest, (0, 1),))

    return edge_map


def get_longest_path(grid):
    paths_lengths = get_paths_lengths(grid)

    edge_list = []
    for src, dests in paths_lengths.items():
        for d, cost in dests.items():
            edge_list.append((src, d, {"cost": cost}))

    G = nx.DiGraph(edge_list)
    return nx.dag_longest_path(G), nx.dag_longest_path_length(G, weight="cost")




if __name__ == "__main__":
    with open("../inputs/2023/23.txt") as f:
        grid = [line.strip() for line in f.readlines()]

    test_data = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
    """
    grid = [line.strip() for line in test_data.strip().splitlines()]
    
    # part 1
    longest_path, long_len = get_longest_path(grid)
    print(longest_path, long_len)
