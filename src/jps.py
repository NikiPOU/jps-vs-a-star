from heapq import heappush, heappop

def is_passable(grid, x, y):
    """
    Check if a cell at coordinates (x, y) is within grid bounds and walkable.

    Parameters:
    grid (list of list of int): 2D grid representing the map (0 = walkable, 1 = wall)
    x (int): Row index
    y (int): Column index

    Returns:
    bool: True if the cell is walkable and within bounds, else False
    """
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

def jump(grid, x, y, dx, dy, goal):
    """
    Perform the Jump Point Search jump function from a starting point in a given direction.

    Parameters:
    grid (list of list of int): The 2D map
    x, y (int): Current cell coordinates
    dx, dy (int): Direction to jump (-1, 0, or 1)
    goal (tuple): Goal coordinates (row, col)

    Returns:
    tuple or None: Coordinates of a jump point, or None if no jump point found
    """
    nx, ny = x + dx, y + dy
    if not is_passable(grid, nx, ny):
        return None

    if (nx, ny) == goal:
        return (nx, ny)

    # Diagonal pruning
    if dx != 0 and dy != 0:
        if (not is_passable(grid, nx - dx, ny) or not is_passable(grid, nx, ny - dy)):
            return None
        if jump(grid, nx, ny, dx, 0, goal) or jump(grid, nx, ny, 0, dy, goal):
            return (nx, ny)

    # Horizontal pruning
    if dx != 0 and dy == 0:
        if (is_passable(grid, nx, ny+1) and not is_passable(grid, x, y+1)) or \
           (is_passable(grid, nx, ny-1) and not is_passable(grid, x, y-1)):
            return (nx, ny)

    # Vertical pruning
    if dy != 0 and dx == 0:
        if (is_passable(grid, nx+1, ny) and not is_passable(grid, x+1, y)) or \
           (is_passable(grid, nx-1, ny) and not is_passable(grid, x-1, y)):
            return (nx, ny)

    # proceed jumping in the same direction
    return jump(grid, nx, ny, dx, dy, goal)

def get_successors(grid, node, goal):
    """
    Get all jump point successors of the current node.

    Parameters:
    grid (list of list of int): The 2D map
    node (tuple): Current node coordinates (row, col)
    goal (tuple): Goal coordinates (row, col)

    Returns:
    list of tuple: List of jump point coordinates reachable from the current node
    """
    x, y = node
    successors = []
    directions = [(-1,0), (1,0), (0,-1), (0,1),
                  (-1,-1), (-1,1), (1,-1), (1,1)]
    for dx, dy in directions:
        jp = jump(grid, x, y, dx, dy, goal)
        if jp:
            successors.append(jp)
    return successors

def heuristic(a, b):
    """
    Calculate Manhattan distance between two points.

    Parameters:
    a (tuple): Coordinates of first point (row, col)
    b (tuple): Coordinates of second point (row, col)

    Returns:
    int: Manhattan distance
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(start, goal, grid):
    """
    Find the shortest path from start to goal using JPS.

    Parameters:
    start (tuple): Starting coordinates (row, col)
    goal (tuple): Goal coordinates (row, col)
    grid (list of list of int): 2D grid representing the map (0 = walkable, 1 = wall)

    Returns:
    list of tuple: Ordered list of coordinates representing the shortest path from start to goal.
                   Returns an empty list if no path exists.
    """
    open_set = []
    heappush(open_set, (heuristic(start, goal), start))
    came_from = {}  # each node mapped to its parent
    cost_so_far = {start: 0}  # Cost from start to each node

    while open_set:
        _, current = heappop(open_set)

        # goal reached so reconstruct path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Return path from start to goal

        # Explore successors
        for neighbor in get_successors(grid, current, goal):
            new_cost = cost_so_far[current] + 1
            if new_cost < cost_so_far.get(neighbor, float("inf")):
                came_from[neighbor] = current
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heappush(open_set, (priority, neighbor))

    # No path found
    return []
