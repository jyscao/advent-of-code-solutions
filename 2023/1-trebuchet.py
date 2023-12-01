def calibrate1(input_lines):
    res = 0
    for line in input_lines:
        for c in line:
            if c.isdigit():
                a = c
                break
        for c in line[::-1]:
            if c.isdigit():
                b = c
                break
        res += int(a + b)
    return res


word_num_map = {
    "one":   "1",
    "two":   "2",
    "three": "3",
    "four":  "4",
    "five":  "5",
    "six":   "6",
    "seven": "7",
    "eight": "8",
    "nine":  "9",
}

def calibrate2(input_lines):
    res = 0
    for line in input_lines:
        for i, c in enumerate(line):
            if c.isdigit():
                a = c
                break
            else:
                found = False
                for k, v in word_num_map.items():
                    if line.startswith(k, i):
                        a = v
                        found = True
                        break
                if found:
                    break
        line_rev = line[::-1]
        for i, c in enumerate(line_rev):
            if c.isdigit():
                b = c
                break
            else:
                found = False
                for k, v in word_num_map.items():
                    if line_rev.startswith(k[::-1], i):
                        b = v
                        found = True
                        break
                if found:
                    break
        res += int(a + b)
    return res


if __name__ == "__main__":
    with open("../inputs/2023/1.txt") as f:
        aoc_input_1 = f.read().strip().split('\n')

    ans1 = calibrate1(aoc_input_1)
    ans2 = calibrate2(aoc_input_1)
    print(ans1, ans2)
