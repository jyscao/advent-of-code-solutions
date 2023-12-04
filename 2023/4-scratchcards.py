from collections import Counter

def scratch1(data):
    res = 0
    for wins, haves in data.values():
        n_match = len(wins.intersection(haves))
        if n_match:
            res += 2 ** (n_match - 1)
    return res


def scratch2(data):
    card_counts = Counter({card_id: 1 for card_id in data.keys()})
    for card, (wins, haves) in data.items():
        n_match = len(wins.intersection(haves))
        for i in range(card + 1, card + n_match + 1):
            card_counts[i] += card_counts[card]

    return card_counts.total()



if __name__ == "__main__":
#     raw_data = """
# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
#     """
#     data = {
#         int(card_id.split()[1]):
#         tuple(set(c.split()) for c in cards.strip().split("|", maxsplit=1))
#         for card_id, cards in (line.strip().split(":", maxsplit=1) for line in raw_data.strip().split("\n"))
#     }

    with open("../inputs/2023/4.txt") as f:
        data = {
            int(card_id.split()[1]):
            tuple(set(c.split()) for c in cards.strip().split("|", maxsplit=1))
            for card_id, cards in (line.strip().split(":", maxsplit=1) for line in f.readlines())
        }
        assert all(len(wins) == 10 and len(haves) == 25 for wins, haves in data.values())

    print(scratch1(data))
    print(scratch2(data))
