import heapq


def find_neighbors1(grid, curr_cost, curr_pos, src_dir):
    N = len(grid)
    x, y = curr_pos
    sx, sy = src_dir

    reachables = []
    if sx and not sy:
        cost_l, cost_r = 0, 0
        for j in range(1, 4):
            dir_l, dir_r = -1 * sx, 1 * sx
            (_, yl), (_, yr) = left, right = (x, y + (dir_l * j)), (x, y + (dir_r * j))
            if 0 <= yl < N:
                cost_l += grid[x][yl]
                reachables.append((curr_cost + cost_l, left, (0, dir_l)))
            if 0 <= yr < N:
                cost_r += grid[x][yr]
                reachables.append((curr_cost + cost_r, right, (0, dir_r)))
    elif not sx and sy:
        cost_l, cost_r = 0, 0
        for i in range(1, 4):
            dir_l, dir_r = 1 * sy, -1 * sy
            (xl, _), (xr, _) = left, right = (x + (dir_l * i), y), (x + (dir_r * i), y)
            if 0 <= xl < N:
                cost_l += grid[xl][y]
                reachables.append((curr_cost + cost_l, left, (dir_l, 0)))
            if 0 <= xr < N:
                cost_r += grid[xr][y]
                reachables.append((curr_cost + cost_r, right, (dir_r, 0)))
    else:
        raise Exception("this should never be reached!")

    return reachables
    

def find_neighbors2(grid, curr_cost, curr_pos, src_dir):
    N = len(grid)
    x, y = curr_pos
    sx, sy = src_dir

    reachables = []
    if sx and not sy:
        cost_l, cost_r = 0, 0
        for j in range(1, 11):
            dir_l, dir_r = -1 * sx, 1 * sx
            (_, yl), (_, yr) = left, right = (x, y + (dir_l * j)), (x, y + (dir_r * j))

            if 0 <= yl < N:
                cost_l += grid[x][yl]
                if j >= 4:
                    reachables.append((curr_cost + cost_l, left, (0, dir_l)))
            if 0 <= yr < N:
                cost_r += grid[x][yr]
                if j >= 4:
                    reachables.append((curr_cost + cost_r, right, (0, dir_r)))
    elif not sx and sy:
        cost_l, cost_r = 0, 0
        for i in range(1, 11):
            dir_l, dir_r = 1 * sy, -1 * sy
            (xl, _), (xr, _) = left, right = (x + (dir_l * i), y), (x + (dir_r * i), y)

            if 0 <= xl < N:
                cost_l += grid[xl][y]
                if i >= 4:
                    reachables.append((curr_cost + cost_l, left, (dir_l, 0)))
            if 0 <= xr < N:
                cost_r += grid[xr][y]
                if i >= 4:
                    reachables.append((curr_cost + cost_r, right, (dir_r, 0)))
    else:
        raise Exception("this should never be reached!")

    return reachables


def init_edges_map_and_pq(grid, nb_find_fn):
    src_neighbors = []
    for dir in {(1, 0), (0, 1)}:
        src_neighbors.extend(nb_find_fn(grid, 0, (0, 0), dir))

    edges_map = {(0, 0): {}}
    for cost, n_pos, src_dir in src_neighbors:
        edges_map[(0, 0)][(n_pos, src_dir)] = cost

    heapq.heapify(src_neighbors)
    return edges_map, src_neighbors


def search_cheapest_to_destination(grid, nb_find_fn):
    N = len(grid)
    destination = (N - 1, N - 1)

    edges_map, cost_pq = init_edges_map_and_pq(grid, nb_find_fn)
    curr_cost, curr_pos = -1, (0, 0)
    while cost_pq:
        curr_cost, curr_pos, _ = node_state = heapq.heappop(cost_pq)
        if curr_pos == destination:
            break

        if curr_pos not in edges_map:
            edges_map[curr_pos] = {}
        curr_nb_edges = edges_map[curr_pos]

        for nb_cost, nb_pos, nb_dir in nb_find_fn(grid, *node_state):
            edge_key = (nb_pos, nb_dir)
            if edge_key in curr_nb_edges:
                old_cost = edges_map[curr_pos][edge_key]
                if nb_cost < old_cost:
                    edges_map[curr_pos][edge_key] = min(old_cost, nb_cost)
                    old_pq_idx = cost_pq.index((old_cost, *edge_key))
                    cost_pq[old_pq_idx] = (nb_cost, *edge_key)
                    heapq.heapify(cost_pq)
            else:
                edges_map[curr_pos][edge_key] = nb_cost
                heapq.heappush(cost_pq, (nb_cost, nb_pos, nb_dir))

    return curr_cost




if __name__ == "__main__":
    with open("../inputs/2023/17.txt") as f:
        grid = [[int(d) for d in list(line.strip())] for line in f.readlines()]

    test_data = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
    """
    # grid = [[int(d) for d in list(line.strip())] for line in test_data.strip().splitlines()]

    # part 1
    lowest_cost1 = search_cheapest_to_destination(grid, find_neighbors1)
    print(lowest_cost1)

    # part 2
    lowest_cost2 = search_cheapest_to_destination(grid, find_neighbors2)
    print(lowest_cost2)
