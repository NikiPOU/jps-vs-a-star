from heapq import heappush, heappop
import math

def passable(grid, x, y):
    """
    Check if a cell is within bounds and walkable.

    Parameters:
    grid (list of list of int): 2D grid map (0=walkable, 1=wall)
    x (int): Row index
    y (int): Column index

    Returns:
    bool: True if the cell is walkable and inside the grid
    """
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

def jump(grid, x, y, dx, dy, goal):
    """
    Recursive jump function for JPS.
    Skips over nodes in straight or diagonal direction until
    a forced neighbor or the goal is reached.

    Parameters:
    grid (list of list of int): 2D grid
    x, y (int): Current cell coordinates
    dx, dy (int): Direction of movement
    goal (tuple): Goal coordinates

    Returns:
    tuple or None: Next jump point coordinates or None if blocked
    """
    nx, ny = x + dx, y + dy
    if not passable(grid, nx, ny):
        return None
    if (nx, ny) == goal:
        return (nx, ny)
    
    # Diagonal forced neighbors
    if dx != 0 and dy != 0:
        if (passable(grid, nx - dx, ny + dy) and not passable(grid, nx - dx, ny)) or \
           (passable(grid, nx + dx, ny - dy) and not passable(grid, nx, ny - dy)):
            return (nx, ny)
        if jump(grid, nx, ny, dx, 0, goal) or jump(grid, nx, ny, 0, dy, goal):
            return (nx, ny)
    elif dx != 0:
        if (passable(grid, nx, ny + 1) and not passable(grid, x, y + 1)) or \
           (passable(grid, nx, ny - 1) and not passable(grid, x, y - 1)):
            return (nx, ny)
    elif dy != 0:
        if (passable(grid, nx + 1, ny) and not passable(grid, x + 1, y)) or \
           (passable(grid, nx - 1, ny) and not passable(grid, x - 1, y)):
            return (nx, ny)

    return jump(grid, nx, ny, dx, dy, goal)

def successors(grid, node, goal):
    """
    Get all jump point successors from the current node.

    Parameters:
    grid (list of list of int): 2D grid
    node (tuple): Current node coordinates
    goal (tuple): Goal coordinates

    Returns:
    list of tuples: Jump points reachable from the node
    """
    x, y = node
    dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    return [jp for dx, dy in dirs if (jp := jump(grid, x, y, dx, dy, goal))]

def heuristic(a, b):
    """
    Octile distance heuristic for 8-directional movement.

    Parameters:
    a, b (tuple): Coordinates (row, col)

    Returns:
    float: Estimated cost between a and b
    """
    dx, dy = abs(a[0]-b[0]), abs(a[1]-b[1])
    return max(dx, dy) + (math.sqrt(2)-1)*min(dx, dy)

def reconstruct(came_from, start, goal):
    """
    Reconstruct the full path from start to goal using jump points.
    Includes intermediate steps along straight or diagonal lines.

    Parameters:
    came_from (dict): Mapping of node -> parent node
    start, goal (tuple): Start and goal coordinates

    Returns:
    list of tuples: Full path from start to goal
    """
    path = [goal]
    current = goal
    while current != start:
        parent = came_from[current]
        dx, dy = parent[0]-current[0], parent[1]-current[1]
        steps = max(abs(dx), abs(dy))
        sx, sy = dx//steps, dy//steps
        for i in range(1, steps):
            path.append((current[0]+sx*i, current[1]+sy*i))
        path.append(parent)
        current = parent
    return path[::-1]

def find_path(start, goal, grid):
    """
    Find a path from start to goal using Jump Point Search (JPS).

    Parameters:
    start, goal (tuple): Start and goal coordinates
    grid (list of list of int): 2D grid map

    Returns:
    list of tuples or None: Path from start to goal including intermediate steps,
                            or None if no path exists
    """
    open_set = [(heuristic(start, goal), start)]
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, current = heappop(open_set)
        if current == goal:
            return reconstruct(came_from, start, goal)

        for n in successors(grid, current, goal):
            step_cost = math.sqrt(2) if n[0]-current[0] != 0 and n[1]-current[1] != 0 else 1
            new_cost = cost_so_far[current]+step_cost
            if new_cost < cost_so_far.get(n, float("inf")):
                came_from[n] = current
                cost_so_far[n] = new_cost
                heappush(open_set, (new_cost+heuristic(n, goal), n))

    return None
