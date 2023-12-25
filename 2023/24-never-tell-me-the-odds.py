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


def get_mat_coeffs_and_b(pos_vel_ls):
    vec_pairs = [(0, 1), (0, 2)]
    A, b = [], []
    for i, j in vec_pairs:
        (pi_x, pi_y, pi_z), (vi_x, vi_y, vi_z) = pos_vel_ls[i]
        (pj_x, pj_y, pj_z), (vj_x, vj_y, vj_z) = pos_vel_ls[j]

        x_vec = [0, (vi_z - vj_z), (vj_y - vi_y), 0, (pj_z - pi_z), (pi_y - pj_y)]
        y_vec = [(vj_z - vi_z), 0, (vi_x - vj_x), (pi_z - pj_z), 0, (pj_x - pi_x)]
        z_vec = [(vi_y - vj_y), (vj_x - vi_x), 0, (pj_y - pi_y), (pi_x - pj_x), 0]

        x_b = pi_y * vi_z - pi_z * vi_y - pj_y * vj_z + pj_z * vj_y
        y_b = pi_z * vi_x - pi_x * vi_z - pj_z * vj_x + pj_x * vj_z
        z_b = pi_x * vi_y - pi_y * vi_x - pj_x * vj_y + pj_y * vj_x

        A += [x_vec, y_vec, z_vec]
        b += [x_b, y_b, z_b]

    return A, b





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

    # hail_pos_vel = extract_data(test_data)
    # bounds = (7, 27)
    # print(hail_pos_vel)

    # part 1
    n_intersects = count_intersects(hail_pos_vel, bounds)
    print(n_intersects)
    # 14673 is too high, 14671 is too low -> likely some floating point
    # arithmetic error causing the program to miss the correct answer of 14672

    # part 2 amazing insight from Reddit:
    # https://www.reddit.com/r/adventofcode/comments/18pnycy/2023_day_24_solutions/kepu26z/
    # 
    # P_r + t_i * V_r == P_i + t_i * V_i, for all i, where P_r & V_r are the
    # position & velocity vectors for the rock, P_i & V_i are for each
    # hailstone, t_i is the collision times for each
    #
    # rearranging: P_r - P_i == -t_i * (V_r - V_i) 
    #
    # then take the product for both sides with (V_r - V_i) gives:
    # (P_r - P_i) × (V_r - V_i) == 0, where 0 is the zero vector
    #
    # expand: P_r × V_r - P_r × V_i - P_i × V_r + P_i × V_i == 0 
    # thus: P_r × V_r = P_r × V_i + P_i × V_r - P_i × V_i, for all i
    #
    # next we choose 2 pairs of i's, e.g. (0, 1) & (0, 2), and equate (x, y, z)
    # components of the resulting expanded cross-product equation, to get 6
    # equations for the 6 unknowns of (pr_x, pr_y, pr_z, vr_x, vr_y, vr_z)
    A, b = get_mat_coeffs_and_b(hail_pos_vel)
    #
    # finally a standard linear solver can be used to obtain the solutions
    eigenv = np.linalg.solve(A, b)
    print(eigenv, int(np.round(sum(eigenv[:3]))))
