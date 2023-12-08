from collections import Counter

def calc_earnings(hands_map, bids):
    res = 0
    hands_ordered = (ctup for same_hand in hands_map.values() for ctup in same_hand)
    for r, (_, c) in enumerate(hands_ordered, start=1):
        res += r * bids[c]
    return res


def _eval_hand(card_tup, hands_map):
    counts, hand = card_tup
    if any(n == 5 for n in counts.values()):
        hands_map["five_of_kind"].append(hand)
    elif any(n == 4 for n in counts.values()):
        hands_map["four_of_kind"].append(hand)
    elif len(counts) == 2:
        hands_map["full_house"].append(hand)
    elif any(n == 3 for n in counts.values()):
        hands_map["three_of_kind"].append(hand)
    elif len(counts) == 3:
        hands_map["two_pair"].append(hand)
    elif any(n == 2 for n in counts.values()):
        hands_map["one_pair"].append(hand)
    else:
        hands_map["high_card"].append(hand)


def translate_hand(hand):
    trans_table = str.maketrans({
        '2': 'a',
        '3': 'b',
        '4': 'c',
        '5': 'd',
        '6': 'e',
        '7': 'f',
        '8': 'g',
        '9': 'h',
        'T': 'i',
        'J': 'j',
        'Q': 'k',
        'K': 'l',
        'A': 'm',
    })
    return hand.translate(trans_table)


def get_most_common_non_joker(card_count):
    for c, n in card_count.most_common():
        if c != "J":
            return n
    return 0

def eval_hand_wo_jokers(card_tup):
    counts, _ = card_tup
    no_J_counts = Counter({c: n for c, n in counts.items() if c != "J"})
    if any(n == 4 for n in no_J_counts.values()):
        return "four_of_kind"
    elif any(n == 3 for n in no_J_counts.values()):
        return "three_of_kind"
    elif all(n == 2 for n in no_J_counts.values()):
        return "two_pair"
    elif any(n == 2 for n in no_J_counts.values()):
        return "one_pair"
    else:
        return "high_card"


def _eval_hand_w_joker(card_tup, hands_map):
    counts, hand = card_tup
    if 'J' not in counts:
        _eval_hand(card_tup, hands_map)
    else:
        no_J_hand = eval_hand_wo_jokers(card_tup)
        nJ, nnJ = counts['J'], get_most_common_non_joker(counts)
        high_count = nJ + nnJ

        if no_J_hand == "two_pair" and nJ == 1:
            hands_map["full_house"].append(hand)
        elif high_count == 5:
            hands_map["five_of_kind"].append(hand)
        elif high_count == 4:
            hands_map["four_of_kind"].append(hand)
        elif high_count == 3:
            hands_map["three_of_kind"].append(hand)
        elif high_count == 2:
            hands_map["one_pair"].append(hand)
        else:
            # print(no_J_hand, nJ, nnJ, high_count)
            raise Exception("this should never be reached!")


def translate_hand_w_joker(hand):
    trans_table = str.maketrans({
        'J': '_',
        '2': 'a',
        '3': 'b',
        '4': 'c',
        '5': 'd',
        '6': 'e',
        '7': 'f',
        '8': 'g',
        '9': 'h',
        'T': 'i',
        'Q': 'k',
        'K': 'l',
        'A': 'm',
    })
    return hand.translate(trans_table)

if __name__ == "__main__":
    with open("../inputs/2023/7.txt") as f:
        raw_cards, bids = zip(*(line.strip().split() for line in f.readlines()))
        cards = [(Counter(c), (translate_hand(c), i)) for i, c in enumerate(raw_cards)]
        bids = [int(b) for b in bids]

    hands_map = {
        "high_card":     [],
        "one_pair":      [],
        "two_pair":      [],
        "three_of_kind": [],
        "full_house":    [],
        "four_of_kind":  [],
        "five_of_kind":  [],
    }

    for ct in cards:
        _eval_hand(ct, hands_map)

    for same_hand_cards in hands_map.values():
        same_hand_cards.sort(key=lambda c: c[0])


    earnings = calc_earnings(hands_map, bids)
    print(earnings)


    # part 2:
    # cards_w_joker = [(Counter(c), (translate_hand_w_joker(c), i)) for i, c in enumerate(raw_cards)]
    cards_w_joker = [(Counter(c), (c, i)) for i, c in enumerate(raw_cards)]

    hands_map_w_joker = {
        "high_card":     [],
        "one_pair":      [],
        "two_pair":      [],
        "three_of_kind": [],
        "full_house":    [],
        "four_of_kind":  [],
        "five_of_kind":  [],
    }

    for ct in cards_w_joker:
        _eval_hand_w_joker(ct, hands_map_w_joker)
    # hand_type = 'high_card'
    # print(hands_map_w_joker[hand_type], len(hands_map_w_joker[hand_type]))

    for same_hand_cards in hands_map_w_joker.values():
        same_hand_cards.sort(key=lambda c: c[0])

    earnings_w_joker = calc_earnings(hands_map_w_joker, bids)
    print(earnings_w_joker)
