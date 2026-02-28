import sys
import os
import math

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from a_star import find_path as a_star_path
from jps import find_path as jps_path

#octile distance
def octile_distance(a, b):
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

def test_octile_distance():
    a, b = (0, 0), (3, 4)
    dist = octile_distance(a, b)
    dx, dy = abs(a[0]-b[0]), abs(a[1]-b[1])
    expected = max(dx, dy) + (math.sqrt(2)-1) * min(dx, dy)
    assert abs(dist - expected) < 1e-6, f"Octile distance failed: {dist} != {expected}"
    print("Octile distance test passed.")


#small grid unit tests
def small_grid_tests():
    grids = [
        {
            "name": "4x4 simple",
            "grid": [
                [0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ],
            "start": (0, 0),
            "goal": (3, 3),
            "expected_path_len": 6
        },
        {
            "name": "5x5 diagonal block",
            "grid": [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ],
            "start": (0, 0),
            "goal": (4, 4),
            "expected_path_len": 8
        }
    ]

    for g in grids:
        print(f"\n--- Testing grid: {g['name']} ---")
        # Forward path
        a_path = a_star_path(g["start"], g["goal"], g["grid"])
        j_path = jps_path(g["start"], g["goal"], g["grid"])
        validate_paths(a_path, j_path, g["grid"], g["start"], g["goal"])

        # Reverse path
        a_rev = a_star_path(g["goal"], g["start"], g["grid"])
        j_rev = jps_path(g["goal"], g["start"], g["grid"])
        validate_paths(a_rev, j_rev, g["grid"], g["goal"], g["start"])

#path validation
def validate_paths(path_a, path_j, grid, start, goal):
    assert path_a is not None, "A* failed to find path"
    assert path_j is not None, "JPS failed to find path"

    assert path_a[0] == start and path_a[-1] == goal
    assert path_j[0] == start and path_j[-1] == goal

    assert is_valid_path(path_a, grid), "A* path invalid"
    assert is_valid_path(path_j, grid), "JPS path invalid"

    cost_a = path_cost(path_a)
    cost_j = path_cost(path_j)

    print(f"Start {start} -> Goal {goal} | A* cost: {cost_a}, JPS cost: {cost_j}")
    assert abs(cost_a - cost_j) < 1e-6, "Cost mismatch between A* and JPS"


def is_valid_path(path, grid):
    for i in range(len(path) - 1):
        if not is_straight_line(path[i], path[i+1]):
            return False
        for c in intermediate_cells(path[i], path[i+1]):
            if grid[c[0]][c[1]] != 0:
                return False
    return True

def is_straight_line(a, b):
    dx = abs(a[0]-b[0])
    dy = abs(a[1]-b[1])
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
    for s in range(1, steps):
        cells.append((x1 + s*step_x, y1 + s*step_y))
    return cells

def path_cost(path):
    cost = 0
    for i in range(len(path)-1):
        dx = abs(path[i+1][0] - path[i][0])
        dy = abs(path[i+1][1] - path[i][1])
        if dx > 0 and dy > 0:
            cost += math.sqrt(2)
        else:
            cost += 1
    return round(cost, 6)


def print_jump_points(path):
    print("Jump Points:", path)

if __name__ == "__main__":
    test_octile_distance()
    small_grid_tests()
