def roll_rocks_once_N(data):
    n = len(data)
    data_T = ["".join(r) for r in zip(*data)]

    rolled = []
    for col in data_T:
        new_col, space = "", 0
        for thing in col:
            if thing == "O":
                new_col += thing
            elif thing == ".":
                space += 1
            elif thing == "#":
                new_col += f"{'.' * space}#"
                space = 0
        new_col += "." * space
        assert len(new_col) == n
        rolled.append(new_col)

    return ["".join(x) for x in zip(*rolled)]


def roll_single(full_seg, is_reverse):
    def roll_segment(r, n, is_reverse):
        rocks, dots = 'O' * r, '.' * (n - r)
        return f"{dots}{rocks}" if is_reverse else f"{rocks}{dots}"

    segs = ((seg.count("O"), len(seg)) for seg in full_seg.split("#"))
    rolled = "#".join(roll_segment(*seg_tup, is_reverse) for seg_tup in segs)
    return rolled


def roll_all(dish, dir):
    is_reverse = dir in {'S', 'E'}
    return (roll_single(full_seg, is_reverse) for full_seg in dish)


def spin_once(dish):
    for dir in ('N', 'W', 'S', 'E',):
        dish = roll_all(("".join(fs) for fs in zip(*dish)), dir)
    return dish


def get_final_state(data, n_spins):
    def find_cycle(state):
        all_states, i = [], -1
        while True:
            all_states.append(state)
            state = tuple(spin_once(state))
            if state in all_states:
                i = all_states.index(state)
                break
        return i, all_states
    cycle_start, all_states = find_cycle(data)
    cycle_length = len(all_states) - cycle_start
    idx = (n_spins - cycle_start) % cycle_length + cycle_start
    return all_states[idx]


def calc_load(final_state):
    n = len(final_state)
    res = 0
    for i, col in enumerate(final_state):
        res += (n - i) * col.count("O")
    return res



if __name__ == "__main__":
    with open("../inputs/2023/14.txt") as f:
        data = [line.strip() for line in f.readlines()]

    test_data = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
    """
    # data = [line.strip() for line in test_data.strip().splitlines()]

    # part 1
    print(calc_load(roll_rocks_once_N(data)))

    # part 2
    final_state = get_final_state(data, 1_000_000_000)
    print(calc_load(final_state))
