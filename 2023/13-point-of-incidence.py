from collections import Counter

def calc_value(block, is_vert=False):
    m = len(block)

    ref_plane = Counter()
    for i in range(m):
        pairs = [r1 == r2 for r1, r2 in zip(block[:i][::-1], block[i:])]
        if all(pairs):
            ref_plane[i] += sum(pairs)

    return ref_plane.most_common(1)[0][0] * (1 if is_vert else 100) if ref_plane else None


def get_reflection_value(block):
    h_val = calc_value(block)
    if h_val:
        return h_val

    block_T = ["".join(col) for col in zip(*block)]
    v_val = calc_value(block_T, True)
    if v_val:
        return v_val

    raise Exception("this shouldn't be reached!")


def calc_smudge_val(block, is_vert=False):
    m = len(block)

    def calc_diff(r1, r2):
        diff = 0
        for i in range(len(r1)):
            if r1[i] != r2[i]:
                diff += 1
        return diff

    for i in range(m):
        diffs = [calc_diff(r1, r2) for r1, r2 in zip(block[:i][::-1], block[i:])]
        if sum(diffs) == 1:
            return i * (1 if is_vert else 100)


def get_smudge_value(block):
    h_val = calc_smudge_val(block)
    if h_val:
        return h_val

    block_T = ["".join(col) for col in zip(*block)]
    v_val = calc_smudge_val(block_T, True)
    if v_val:
        return v_val

    raise Exception("this shouldn't be reached!")


if __name__ == "__main__":
    with open("../inputs/2023/13.txt") as f:
        data = [block.splitlines() for block in f.read().strip().split("\n\n")]

    part1, part2 = 0, 0
    for block in data:
        part1 += get_reflection_value(block)
        part2 += get_smudge_value(block)
    print(part1)
    print(part2)
