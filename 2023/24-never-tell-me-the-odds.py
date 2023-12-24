import numpy as np


def extract_data(data):
    split_cast = lambda vec_str: tuple(int(d) for d in (vec_str.strip().split(', ')))
    return [(split_cast(pos_str), split_cast(vel_str))
        for pos_str, vel_str in (line.split("@") for line in data.strip().splitlines())]


def get_A_and_b(pos_vel_ls):
    def get_coeffs_and_intercept(pos, vel):
        x, y, _ = pos
        vx, vy, _ = vel
        xs, ys = (x, x + vx), (y, y + vy)
        m, b = np.polyfit(xs, ys, 1)
        return -m, b

    coeffs_mat, b_vec = [], []
    for pos, vel in pos_vel_ls:
        a_x, b = get_coeffs_and_intercept(pos, vel)
        coeffs_mat.append([a_x, 1])
        b_vec.append(b)
    return coeffs_mat, b_vec


def count_intersects(pos_vel_ls, bounds):
    lower, upper = bounds
    A, b = get_A_and_b(pos_vel_ls)

    def check_if_in_future(idx, x_int, y_int):
        (px, py, _), (vx, vy, _) = pos_vel_ls[idx]
        x_in_the_future = vx > 0 and px < x_int or vx < 0 and px > x_int
        y_in_the_future = vy > 0 and py < y_int or vy < 0 and py > y_int
        if x_in_the_future and y_in_the_future:
            return True
        else:
            return False

    res = 0
    collision_points = set()
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            try:
                mat, bv = [A[i], A[j]], [b[i], b[j]]
                x_int, y_int = np.linalg.solve(mat, bv)
                if lower <= x_int <= upper and lower <= y_int <= upper and all(check_if_in_future(idx, x_int, y_int) for idx in {i, j}):
                    res += 1
                    collision_points.add((x_int, y_int))
            except np.linalg.LinAlgError:
                pass

    return len(collision_points)





if __name__ == "__main__":
    with open("../inputs/2023/24.txt") as f:
        data = f.read()
    hail_pos_vel = extract_data(data)
    bounds = (200_000_000_000_000, 400_000_000_000_000)

    test_data = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
    """

    hail_pos_vel = extract_data(test_data)
    bounds = (7, 27)

    # print(hail_pos_vel)

    # part 1
    n_intersects = count_intersects(hail_pos_vel, bounds)
    print(n_intersects)
    # 14673 is too high, 14671 is too low -> likely some floating point
    # arithmetic error that caused the program to miss the correct answer of
    # 14672
