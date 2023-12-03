from collections import Counter

def cube1(game_data):
    standard = Counter({"red": 12, "green": 13, "blue": 14})

    res = 0
    for id, rounds in game_data:
        if all(r <= standard for r in rounds):
            res += id

    return res


def cube2(game_data):
    res = 0
    colors = ("red", "green", "blue",)

    for _, rounds in game_data:
        power = 1
        for c in colors:
            power *= max(r[c] for r in rounds)
        res += power

    return res


if __name__ == "__main__":
    with open("../inputs/2023/2.txt") as f:
        game_data = [
            (
                int(game_id.split(maxsplit=1)[1]), 
                [Counter({color: int(count) for count, color in [tuple(pair.strip().split()) for pair in round.split(",")]})
                    for round in game_data.strip().split(";")]
            )
            for game_id, game_data in (line.strip().split(":", maxsplit=1) for line in f.readlines())
        ]

    # print(game_data)
    print(cube1(game_data))
    print(cube2(game_data))
