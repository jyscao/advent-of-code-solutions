def predict1(data):
    return sum(predict_next(num_ls) for num_ls in data)

def predict2(data):
    return sum(predict_prev(num_ls) for num_ls in data)

def predict_next(num_ls):
    diffs = [num_ls[i] - num_ls[i-1] for i in range(1, len(num_ls))]
    if all(d == 0 for d in diffs):
        return num_ls[-1]
    else:
        return num_ls[-1] + predict_next(diffs)

def predict_prev(num_ls):
    diffs = [num_ls[i] - num_ls[i-1] for i in range(1, len(num_ls))]
    if all(d == 0 for d in diffs):
        return num_ls[0]
    else:
        return num_ls[0] - predict_prev(diffs)


if __name__ == "__main__":
    with open("../inputs/2023/9.txt") as f:
        data = [[int(i) for i in line.strip().split()] for line in f.readlines()]

    print(predict1(data))
    print(predict2(data))
