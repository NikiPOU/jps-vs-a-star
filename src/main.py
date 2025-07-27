# src/main.py

from a_star import find_path as a_star_path
from jps import find_path as jps_path

def print_grid(grid):
    for row in grid:
        print(" ".join(str(cell) for cell in row))

def main():
    grid = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
    ]
    start = (0, 0)
    goal = (2, 2)

    print("Grid:")
    print_grid(grid)
    print(f"\nStart: {start} | Goal: {goal}")

    a_path = a_star_path(start, goal, grid)
    j_path = jps_path(start, goal, grid)

    print("\nA* Path:", a_path)
    print("JPS Path:", j_path)

if __name__ == "__main__":
    main()
