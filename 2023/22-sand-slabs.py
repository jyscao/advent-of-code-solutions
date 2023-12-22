import numpy as np


def label_bricks(data, start_label):
    start_label = int(start_label, 16)
    return {hex(label_idx)[2:].upper(): bricks for label_idx, bricks in
        enumerate(
            ([(int(x1), int(x2)) for x1, x2 in zip(a.split(','), b.split(','))]
                for a, b in (line.strip().split("~") for line in data.strip().splitlines())),
            start=start_label)
    }


def get_max_dimensions(bricks_map):
    return map(lambda dim_bounds: max(list(zip(*dim_bounds))[-1]),
               list(zip(*bricks_map.values())))


def get_layers_map(bricks_map, z_bound):
    layers_map = {z: set() for z in range(z_bound)}
    for lab, brick_pos in bricks_map.items():
        _, _,(z1, z2) = brick_pos
        for z in range(z1, z2 + 1):
            layers_map[z].add(lab)
    return layers_map


def build_space(bricks_map, layers_map):
    X, Y, Z = map(lambda dim: dim + 1, get_max_dimensions(bricks_map))
    space = np.chararray((Z, Y, X), itemsize=3)
    space.fill('')  # init all elements to the empty string

    for z, bricks in layers_map.items():
        xy_cross = space[z]
        for b_lab in bricks:
            (x1, x2), (y1, y2), _ = bricks_map[b_lab]
            xy_cross[y1:y2+1, x1:x2+1] = b_lab
    return space


def _settle_bricks_and_update_bricks_map(bricks_map, layers_map, bricks_space):
    settled_bricks = set()
    for k, _ in enumerate(bricks_space[2:], start=2):
        for b_lab in layers_map[k]:
            if b_lab not in settled_bricks:
                (x1, x2), (y1, y2), (z1, z2) = bricks_map[b_lab]
                brick_ht = z2 - z1 + 1

                vertical_slice = bricks_space[1:k, y1:y2+1, x1:x2+1]
                drop_amount = find_drop_amount(vertical_slice)

                if drop_amount > 0:
                    empty_block = bricks_space[k-drop_amount:k, y1:y2+1, x1:x2+1]
                    brick_block = bricks_space[k:k+brick_ht, y1:y2+1, x1:x2+1]
                    bricks_space[k-drop_amount:k+brick_ht, y1:y2+1, x1:x2+1] = np.concatenate((brick_block, empty_block))

                    bricks_map[b_lab][2] = (z1 - drop_amount, z2 - drop_amount)
                    settled_bricks.add(b_lab)


def find_drop_amount(vertical_slice):
    drop_amount = 0
    for layer in vertical_slice[::-1]:
        if all(all(x == "" for x in y) for y in layer):
            drop_amount += 1
        else:
            break
    return drop_amount


def get_non_removables(bricks_map, layers_map, bricks_space):
    non_removables = set()

    for k, _ in enumerate(bricks_space[2:], start=2):
        for b_lab in layers_map[k]:
            (x1, x2), (y1, y2), _ = bricks_map[b_lab]
            support_layer = bricks_space[k-1, y1:y2+1, x1:x2+1]
            support_bricks = {sb.decode("utf8") for y in support_layer for sb in y if sb != ""}
            if len(support_bricks) == 1 and (supp_br := support_bricks.pop()) != b_lab:
                non_removables.add(supp_br)
    return non_removables


def calc_n_removables(data, start_label):
    bricks_map = label_bricks(data, start_label)
    _, _, Z = map(lambda dim: dim + 1, get_max_dimensions(bricks_map))
    layers_map = get_layers_map(bricks_map, Z)
    bricks_space = build_space(bricks_map, layers_map)

    # wait for bricks settle
    _settle_bricks_and_update_bricks_map(bricks_map, layers_map, bricks_space)
    settled_layers_map = get_layers_map(bricks_map, Z)
    non_removables = get_non_removables(bricks_map, settled_layers_map, bricks_space)

    return len(set(bricks_map.keys()).difference(non_removables))



if __name__ == "__main__":
    with open("../inputs/2023/22.txt") as f:
        data, start_label = f.read(), "A"

    test_data = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
    """

    data, start_label = test_data, "A"

    # part 1
    n_removables = calc_n_removables(data, start_label)
    print(n_removables)
