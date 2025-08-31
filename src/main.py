import time
from a_star import find_path as a_star_path
from jps import find_path as jps_path

def print_grid(grid, path=None):
    """
    Print the grid to the terminal, optionally highlighting a path.

    Parameters:
    grid (list of list of int): 2D grid (0 = walkable, 1 = wall)
    path (list of tuple, optional): List of coordinates representing the path
    """
    path_set = set(path) if path else set()
    for y, row in enumerate(grid):
        row_str = ""
        for x, cell in enumerate(row):
            if (y, x) in path_set:
                row_str += "• "
            elif cell == 1:
                row_str += "█ "
            else:
                row_str += ". "
        print(row_str)
    print()

def get_user_point(prompt, max_y, max_x, grid):
    """
    Prompt the user for a point (row, col) and validate input.

    Parameters:
    prompt (str): Message to show the user
    max_y (int): Maximum row index
    max_x (int): Maximum column index
    grid (list of list of int): 2D grid for validation

    Returns:
    tuple: Validated coordinates (row, col)
    """
    while True:
        try:
            y, x = map(int, input(f"{prompt} (row col): ").strip().split())
            if not (0 <= y < max_y and 0 <= x < max_x):
                print("Coordinates out of bounds.")
                continue
            if grid[y][x] == 1:
                print("That point is a wall (█). Please choose a walkable space (0).")
                continue
            return (y, x)
        except Exception:
            print("Invalid input. Use two numbers separated by a space.")

def get_user_grid():
    """
    Prompt the user to input a custom grid row by row.

    Returns:
    list of list of int: 2D grid entered by the user
    """
    print("Enter grid rows (use 0 for empty, 1 for wall). Empty line to finish:")
    grid = []
    while True:
        row = input()
        if row.strip() == "":
            break
        try:
            grid.append([int(ch) for ch in row.split()])
        except ValueError:
            print("Invalid input. Use only 0 and 1 separated by spaces.")
    return grid

def print_path_info(name, path, elapsed_time, grid):
    """
    Print the results of a pathfinding algorithm.

    Parameters:
    name (str): Algorithm name ('A*' or 'JPS')
    path (list of tuple): Path found by the algorithm
    elapsed_time (float): Time taken to compute the path
    grid (list of list of int): Grid for displaying the path
    """
    print(f"{name} Path:")
    if path:
        print_grid(grid, path)
        print(f"Steps: {len(path)} | Time: {elapsed_time:.6f}s\n")
    else:
        print_grid(grid)
        print("No path found!\n")

def main():
    """
    Main function to run the pathfinding comparison program.
    """
    print("Welcome to the A* vs JPS Pathfinder!\n")
    print("This tool compares the A* and Jump Point Search (JPS) algorithms for pathfinding.\n")
    print("How it works:")
    print("• The shortest path from a start point to a goal will be found using both algorithms.")
    print("• The number of steps and time taken will be displayed for each algorithm.\n")
    print("Instructions:")
    print("• You can use a default 3x3 grid, or create your own.")
    print("• The grid is a 2D space of walkable (.) and blocked (█) cells.")
    print("• 0 represents walkable space, and 1 represents a wall or obstacle.")
    print("• Input your start and goal points as two integers (row and column), e.g., '0 0'.")
    print("• Points are given in (row, col) format, starting from the top-left corner (0-indexed).\n")

    use_default = input("Use default grid? (yes/no): ").lower() == "yes"
    
    if use_default:
        grid = [
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 0],
        ]
    else:
        grid = get_user_grid()

    max_y, max_x = len(grid), len(grid[0])
    print("\nGrid layout:")
    print_grid(grid)

    start = get_user_point("Enter start point", max_y, max_x, grid)
    goal = get_user_point("Enter goal point", max_y, max_x, grid)

    print(f"\nStart: {start} | Goal: {goal}\n")

    # Run A* algorithm
    start_time = time.perf_counter()
    a_path = a_star_path(start, goal, grid)
    a_time = time.perf_counter() - start_time

    # Run JPS algorithm
    start_time = time.perf_counter()
    j_path = jps_path(start, goal, grid)
    j_time = time.perf_counter() - start_time

    # Print results
    print_path_info("A*", a_path, a_time, grid)
    print_path_info("JPS", j_path, j_time, grid)

if __name__ == "__main__":
    main()
