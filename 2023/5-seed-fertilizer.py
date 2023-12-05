def get_loc1(seeds, garden_maps):
    seed_to_loc = []
    for s in seeds:
        num = s
        for gm in garden_maps.values():
            num = proc_through_map(num, gm)
        seed_to_loc.append(num)
    return min(seed_to_loc)


def get_loc2_brute_force(seeds, garden_maps):
    min_loc = float("inf")
    for ss, sr in seeds:
        for s in range(ss, ss + sr):
            num = s
            for gm in garden_maps.values():
                num = proc_through_map(num, gm)
            min_loc = min(min_loc, num)
    return min_loc


def get_loc2(seeds, garden_maps_rev):
    seed_ranges = [range(ss, ss + sr) for ss, sr in seeds]

    loc_ranges = garden_maps_rev["loc_to_humid"]
    min_start = min(loc_ranges, key=lambda lr: lr[0])[0]
    if min_start > 0:
        loc_ranges[range(0, min_start)] = (0, 0,)
    loc_ranges = sorted(garden_maps_rev["loc_to_humid"].keys(), key=lambda lr: lr[0])

    upper = float("inf")
    for loc_range in loc_ranges:
        num0, num1 = loc_range[0], loc_range[-1]
        for gmr in garden_maps_rev.values():
            num0 = proc_through_map(num0, gmr)
            num1 = proc_through_map(num1, gmr)
        if any(num0 in sr for sr in seed_ranges):
            return loc_range[0]
        if any(num1 in sr for sr in seed_ranges):
            upper = loc_range[-1]
            break

    curr_loc = upper
    while True:
        num = curr_loc
        for gmr in garden_maps_rev.values():
            num = proc_through_map(num, gmr)
        if any(num in sr for sr in seed_ranges):
            curr_loc -= 1
        else:
            return curr_loc + 1


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


def parse_data_maps_rev(data):
    return {
        range(int(dst), int(dst) + int(rl)): (int(dst), int(src))
        for dst, src, rl in (line.split() for line in data.strip().split("\n")[1:])
    }


if __name__ == "__main__":
    # with open("../inputs/2023/5-example.txt") as f:
    with open("../inputs/2023/5.txt") as f:
        data = f.read().strip().split("\n\n")

    seeds1 = [int(s) for s in data[0].strip().split()[1:]]
    garden_maps = {
        "seed_to_soil":   parse_data_maps(data[1]),
        "soil_to_fert":   parse_data_maps(data[2]),
        "fert_to_water":  parse_data_maps(data[3]),
        "water_to_light": parse_data_maps(data[4]),
        "light_to_temp":  parse_data_maps(data[5]),
        "temp_to_humid":  parse_data_maps(data[6]),
        "humid_to_loc":   parse_data_maps(data[7]),
    }
    # print(garden_maps)
    print(get_loc1(seeds1, garden_maps))

    seeds2 = list(zip(seeds1[0::2], seeds1[1::2]))
    garden_maps_rev = {
        "loc_to_humid":   parse_data_maps_rev(data[7]),
        "humid_to_temp":  parse_data_maps_rev(data[6]),
        "temp_to_light":  parse_data_maps_rev(data[5]),
        "light_to_water": parse_data_maps_rev(data[4]),
        "water_to_fert":  parse_data_maps_rev(data[3]),
        "fert_to_soil":   parse_data_maps_rev(data[2]),
        "soil_to_seed":   parse_data_maps_rev(data[1]),
    }
    # print(garden_maps_rev)

    print(get_loc2(seeds2, garden_maps_rev))
    # print(get_loc2_brute_force(seeds2, garden_maps))
