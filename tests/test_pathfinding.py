import time
from src.a_star import find_path as a_star_path
from src.jps import find_path as jps_path

# test for correctness

def test_simple_path():
    grid = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
    ]
    run_correctness_test(grid, (0, 0), (2, 2))


def test_no_path():
    grid = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]
    start, goal = (0, 0), (2, 2)

    assert a_star_path(start, goal, grid) is None
    assert jps_path(start, goal, grid) is None


def test_start_equals_goal():
    grid = [
        [0, 0],
        [0, 0],
    ]
    start = goal = (1, 1)

    assert a_star_path(start, goal, grid) == [start]
    assert jps_path(start, goal, grid) == [start]

def test_larger_open_grid():
    #Open 10x10 grid
    grid = [[0] * 10 for _ in range(10)]
    # adding obstacles
    grid[2][2] = 1
    grid[3][3] = 1
    grid[5][5] = 1
    grid[6][4] = 1
    grid[7][7] = 1

    run_correctness_test(grid, (0, 0), (9, 9))



# performance

def test_performance_a_star():
    grid = [[0 if (i + j) % 3 else 1 for j in range(50)] for i in range(50)]
    start, goal = (0, 0), (49, 49)

    t0 = time.perf_counter()
    path = a_star_path(start, goal, grid)
    t1 = time.perf_counter()

    assert path is None or (path[0] == start and path[-1] == goal)
    print(f"A* runtime: {t1 - t0:.4f} seconds")


def test_performance_jps():
    grid = [[0 if (i + j) % 3 else 1 for j in range(50)] for i in range(50)]
    start, goal = (0, 0), (49, 49)

    t0 = time.perf_counter()
    path = jps_path(start, goal, grid)
    t1 = time.perf_counter()

    assert path is None or (path[0] == start and path[-1] == goal)
    print(f"JPS runtime: {t1 - t0:.4f} seconds")



# helper functions

def run_correctness_test(grid, start, goal):
    a_path = a_star_path(start, goal, grid)
    j_path = jps_path(start, goal, grid)

    assert a_path is not None, "A* failed to find path"
    assert j_path is not None, "JPS failed to find path"

    assert a_path[0] == start and a_path[-1] == goal, "A* path start or end incorrect"
    assert j_path[0] == start and j_path[-1] == goal, "JPS path start or end incorrect"

    assert is_valid_path(a_path, grid), "A* path invalid"
    assert is_valid_path(j_path, grid), "JPS path invalid"

    assert path_cost(a_path) <= path_cost(j_path)


def is_valid_path(path, grid):
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]

        if not is_straight_line(start, end):
            return False

        for cell in intermediate_cells(start, end):
            if grid[cell[0]][cell[1]] != 0:
                return False
    return True


def is_straight_line(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return dx == 0 or dy == 0 or dx == dy


def intermediate_cells(start, end):
    cells = []
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))
    if steps <= 1:
        return cells

    step_x = dx // steps
    step_y = dy // steps

    for step in range(1, steps):
        cells.append((x1 + step * step_x, y1 + step * step_y))
    return cells


def path_cost(path):
    cost = 0
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        dx, dy = end[0] - start[0], end[1] - start[1]
        steps = max(abs(dx), abs(dy))

        step_x = dx // steps if steps != 0 else 0
        step_y = dy // steps if steps != 0 else 0

        for _ in range(steps):
            if step_x != 0 and step_y != 0:
                cost += 1.4
            else:
                cost += 1
    return round(cost, 1)
