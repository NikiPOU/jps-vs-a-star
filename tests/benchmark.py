import sys
import os
import random
import time
import statistics
import math

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from map_loader import load_movingai_map
from a_star import find_path as astar
from jps import find_path as jps


MAP_PATH = "tests/Berlin_1_256.map"
NUM_TESTS = 1000
MIN_DISTANCE = 20
DEBUG_STOP_ON_FAILURE = True


def random_free_cell(grid):
    h = len(grid)
    w = len(grid[0])
    while True:
        y = random.randint(0, h-1)
        x = random.randint(0, w-1)
        if grid[y][x] == 0:
            return (y, x)


def euclidean_distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def compute_path_cost(path):
    cost = 0
    for i in range(1, len(path)):
        dy = abs(path[i][0] - path[i-1][0])
        dx = abs(path[i][1] - path[i-1][1])
        diag = min(dy, dx)
        straight = max(dy, dx) - diag
        cost += diag * math.sqrt(2) + straight
    return cost


def validate_path(grid, path):
    for i in range(1, len(path)):
        y1, x1 = path[i - 1]
        y2, x2 = path[i]

        if abs(y2 - y1) > 1 or abs(x2 - x1) > 1:
            print("Invalid: step larger than 1 cell")
            return False

        if grid[y2][x2] != 0:
            print("Invalid: stepped into obstacle")
            return False

    return True


def print_ascii(grid, path_a, path_j, start, goal, radius=20):
    sy, sx = start
    h = len(grid)
    w = len(grid[0])

    min_y = max(0, sy - radius)
    max_y = min(h, sy + radius)
    min_x = max(0, sx - radius)
    max_x = min(w, sx + radius)

    set_a = set(path_a or [])
    set_j = set(path_j or [])

    print("\n=== ASCII MAP (cropped) ===")
    for y in range(min_y, max_y):
        row = ""
        for x in range(min_x, max_x):
            if (y, x) == start:
                row += "S"
            elif (y, x) == goal:
                row += "G"
            elif (y, x) in set_a and (y, x) in set_j:
                row += "B"
            elif (y, x) in set_a:
                row += "A"
            elif (y, x) in set_j:
                row += "J"
            elif grid[y][x] != 0:
                row += "#"
            else:
                row += "."
        print(row)
    print("===========================\n")


def main():
    grid = load_movingai_map(MAP_PATH)
    print(f"Loaded map: {len(grid)} x {len(grid[0])}\n")

    times_a = []
    times_j = []
    costs_a = []
    costs_j = []

    mismatches = 0
    test_count = 0

    while test_count < NUM_TESTS:
        start = random_free_cell(grid)
        goal = random_free_cell(grid)

        if euclidean_distance(start, goal) < MIN_DISTANCE:
            continue

        t0 = time.perf_counter()
        path_a = astar(start, goal, grid)
        t1 = time.perf_counter()

        t2 = time.perf_counter()
        path_j = jps(start, goal, grid)
        t3 = time.perf_counter()

        #CASE 1: no path exists
        if path_a is None and path_j is None:
            test_count += 1
            continue

        #CASE 2: one path found, the other error
        if (path_a is None) != (path_j is None):
            print("\n========== DISAGREEMENT ==========")
            print("Start:", start)
            print("Goal :", goal)
            print("A* path:", path_a)
            print("JPS path:", path_j)
            print_ascii(grid, path_a, path_j, start, goal)
            return

        #CASE 3: both returned paths
        if not validate_path(grid, path_a) or not validate_path(grid, path_j):
            print("\n========== INVALID PATH ==========")
            print("Start:", start)
            print("Goal :", goal)
            print("A* path:", path_a)
            print("JPS path:", path_j)
            print_ascii(grid, path_a, path_j, start, goal)
            return

        cost_a = compute_path_cost(path_a)
        cost_j = compute_path_cost(path_j)

        times_a.append(t1 - t0)
        times_j.append(t3 - t2)
        costs_a.append(cost_a)
        costs_j.append(cost_j)

        #CASE 4: cost mismatch
        if abs(cost_a - cost_j) > 1e-6:
            mismatches += 1
            print("\n========== COST MISMATCH ==========")
            print("Start:", start)
            print("Goal :", goal)
            print("A* cost :", cost_a)
            print("JPS cost:", cost_j)
            print_ascii(grid, path_a, path_j, start, goal)
            return

        test_count += 1
        if test_count % 50 == 0 or test_count == NUM_TESTS:
            print(f"Completed {test_count}/{NUM_TESTS}")

    print("\n===== BENCHMARK RESULTS =====\n")
    print("Cost mismatches:", mismatches)
    print("\nA* Avg Runtime:", statistics.mean(times_a))
    print("JPS Avg Runtime:", statistics.mean(times_j))
    print("A* Avg Cost:", statistics.mean(costs_a))
    print("JPS Avg Cost:", statistics.mean(costs_j))


if __name__ == "__main__":
    main()
