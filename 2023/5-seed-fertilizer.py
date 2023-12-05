def get_loc1(seeds, garden_maps):
    seed_to_loc = []
    for s in seeds:
        num = s
        for gm in garden_maps.values():
            num = proc_through_map(num, gm)
        seed_to_loc.append(num)
    return min(seed_to_loc)


def get_loc2(seeds, garden_maps):
    min_loc = float("inf")
    for ss, sr in seeds:
        for s in range(ss, ss + sr):
            num = s
            for gm in garden_maps.values():
                num = proc_through_map(num, gm)
            min_loc = min(min_loc, num)
    return min_loc


def proc_through_map(num, next_map):
    for mr, (src, dst) in next_map.items():
        if num in mr:
            return num - src + dst
    return num


def parse_data_maps(data):
    return {
        range(int(src), int(src) + int(rl)): (int(src), int(dst))
        for dst, src, rl in (line.split() for line in data.strip().split("\n")[1:])
    }


if __name__ == "__main__":
    with open("../inputs/2023/5.txt") as f:
        data = f.read().strip().split("\n\n")

    seeds1 = [int(s) for s in data[0].strip().split()[1:]]
    seeds2 = zip(seeds1[0::2], seeds1[1::2])

    garden_maps = {
        "seed_to_soil":   parse_data_maps(data[1]),
        "seed_to_fert":   parse_data_maps(data[2]),
        "fert_to_water":  parse_data_maps(data[3]),
        "water_to_light": parse_data_maps(data[4]),
        "light_to_temp":  parse_data_maps(data[5]),
        "temp_to_humid":  parse_data_maps(data[6]),
        "humid_to_loc":   parse_data_maps(data[7]),
    }

    print(get_loc1(seeds1, garden_maps))
    print(get_loc2(seeds2, garden_maps))
