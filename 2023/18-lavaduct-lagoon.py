class Digger:

    def __init__(self, dig_plan):
        self.y, self.x = [0, 0]
        self.dp = dig_plan
        self.trench_boundary = [(self.y, self.x)]


    def _dig(self):
        for dir, steps, _ in self.dp:
            dy, dx = {
                "U": (-1, 0),
                "D": (1, 0),
                "L": (0, -1),
                "R": (0, 1),
            }[dir]
            for _ in range(steps):
                self.y += dy
                self.x += dx
                self.trench_boundary.append((self.y, self.x))

        self._normalize_boundary()
        assert self.trench_boundary[0] == self.trench_boundary[-1]
        assert len(self.trench_boundary) == len(set(self.trench_boundary)) + 1


    def _normalize_boundary(self):
        Y, X = list(zip(*self.trench_boundary))

        min_x, normed_X = min(X), []
        if min_x == 0:
            normed_X = X
        elif min_x < 0:
            offset_x = abs(min_x)
            for x in X:
                normed_X.append(x + offset_x)
        elif min_x > 0:
            offset_x = -min_x
            for x in X:
                normed_X.append(x + offset_x)
        else:
            raise Exception("this should never be reached!")
        self.x_range = max(normed_X) + 1

        min_y, normed_Y = min(Y), []
        if min_y == 0:
            normed_Y = Y
        elif min_y < 0:
            offset_y = abs(min_y)
            for y in Y:
                normed_Y.append(y + offset_y)
        elif min_y > 0:
            offset_y = -min_y
            for y in Y:
                normed_Y.append(y + offset_y)
        else:
            raise Exception("this should never be reached!")
        self.y_range = max(normed_Y) + 1

        self.trench_boundary = list(zip(normed_Y, normed_X))


    def get_fill_seed(self):
        latitude_map = {i: [] for i in range(self.y_range)}
        for y, x in self.trench_boundary:
            latitude_map[y].append(x)

        for y, xs in latitude_map.items():
            if len(xs) == 2:
                return y, sum(xs) // 2

        return self.y_range // 2, self.x_range // 2


    def _init_dug_grid(self):
        self.dug_grid = [list("." * self.x_range) for _ in range(self.y_range)]
        for y, x in set(self.trench_boundary):
            self.dug_grid[y][x] = "#"


    def add_to_coords_stk(self, nb_pos):
        y, x = nb_pos
        if 0 <= y < self.y_range and 0 <= x < self.x_range and self.dug_grid[y][x] != "#":
            return True
        else:
            return False

    def _fill_interior(self):
        self._init_dug_grid()
        coords_stk = [self.get_fill_seed()]
        while coords_stk:
            y, x = coords_stk.pop()
            self.dug_grid[y][x] = "#"
            neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
            for nb_pos in neighbors:
                if self.add_to_coords_stk(nb_pos):
                    coords_stk.append(nb_pos)

    def calc_total_area(self):
        res = 0
        for row in self.dug_grid:
            res += row.count("#")
        return res

    
    def dig_then_report(self):
        self._dig()

        boundary_capacity = len(set(self.trench_boundary))
        print(f"boundary dug: {boundary_capacity} m2")

        self._fill_interior()
        print(f"total dug area: {self.calc_total_area()} m2")

        print()
        for row in self.dug_grid:
            print("".join(t for t in row))




if __name__ == "__main__":
    with open("../inputs/2023/18.txt") as f:
        dig_plan = [(dir, int(amt), color.strip('()')) for line in f.readlines() for dir, amt, color in [line.strip().split()]]

    test_data = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
    """
    dig_plan = [(dir, int(amt), color.strip('()')) for line in test_data.strip().splitlines() for dir, amt, color in [line.strip().split()]]

    # part 1
    digger = Digger(dig_plan)
    digger.dig_then_report()

    # part 2
