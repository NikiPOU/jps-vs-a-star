import heapq
import math


def passable(grid, y, x):
    """
    Check if position is inside the grid and walkable.

    Parameters:
    grid (list of list of int): 2D grid (0 = walkable, 1 = wall)
    y (int): Row index
    x (int): Column index

    Returns:
    bool: True if the tile is valid and not blocked.
    """
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] == 0


def valid_move(grid,y,x,ny,nx):
    """
    Determine whether movement to new position is allowed.
    """
    return passable(grid,ny,nx)


def heuristic(a, b):
    """
    Calculate the Octile distance between two points.
    """
    dy = abs(a[0]-b[0])
    dx = abs(a[1]-b[1])
    return max(dx, dy) + (math.sqrt(2)-1) * min(dx, dy)


def jump(grid,y,x,dy,dx,goal):
    """
    Jump in a direction until a jump point, forced neighbor,
    or the goal is reached.

    Returns:
    tuple or None: The jump point coordinates if found.
    """
    ny,nx = y+dy,x+dx

    if not valid_move(grid,y,x,ny,nx):
        return None

    if (ny, nx) == goal:
        return (ny,nx)

    if dy != 0 and dx != 0:
        if (not passable(grid,ny - dy,nx) and passable(grid, ny-dy, nx+dx)) or \
           (not passable(grid, ny, nx-dx) and passable(grid, ny+dy, nx-dx)):
            return (ny, nx)

        if jump(grid, ny, nx, dy, 0, goal) is not None:
            return (ny, nx)
        if jump(grid, ny, nx, 0, dx, goal) is not None:
            return (ny, nx)

    elif dx != 0:
        if (not passable(grid, ny-1, nx) and passable(grid, ny-1, nx+dx)) or \
           (not passable(grid, ny+1, nx) and passable(grid, ny+1, nx+dx)):
            return (ny, nx)

    elif dy != 0:
        if (not passable(grid, ny, nx+1) and passable(grid, ny+dy, nx+1)) or \
           (not passable(grid, ny, nx-1) and passable(grid, ny+dy, nx-1)):
            return (ny, nx)

    return jump(grid,ny,nx,dy,dx,goal)


def prune_neighbors(grid, current, parent):
    """
    Reduce neighbor directions based on movement direction.
    (JPS pruning step)

    Returns:
    list of tuple: Directions to explore next.
    """
    y, x = current

    if parent is None:
        return [
            (-1,0), (1,0), (0,-1), (0,1),
            (-1,-1), (-1,1), (1,-1), (1,1)
        ]

    py, px = parent
    dy = y - py
    dx = x - px

    dy = 0 if dy == 0 else dy // abs(dy)
    dx = 0 if dx == 0 else dx // abs(dx)

    directions = []

    if dy != 0 and dx != 0:
        if valid_move(grid, y, x, y+dy, x+dx):
            directions.append((dy, dx))
        if valid_move(grid, y, x, y+dy, x):
            directions.append((dy, 0))
        if valid_move(grid, y, x, y, x+dx):
            directions.append((0, dx))

        if not passable(grid, y-dy, x) and passable(grid, y-dy, x+dx):
            directions.append((-dy, dx))
        if not passable(grid, y, x-dx) and passable(grid, y+dy, x-dx):
            directions.append((dy, -dx))

    elif dx != 0:
        if valid_move(grid, y, x, y, x+dx):
            directions.append((0, dx))

        if not passable(grid, y+1, x) and passable(grid, y+1, x+dx):
            directions.append((1, dx))
        if not passable(grid, y-1, x) and passable(grid, y-1, x+dx):
            directions.append((-1, dx))

    elif dy != 0:
        if valid_move(grid, y, x, y+dy, x):
            directions.append((dy, 0))

        if not passable(grid, y, x+1) and passable(grid, y+dy, x+1):
            directions.append((dy, 1))
        if not passable(grid, y, x-1) and passable(grid, y+dy, x-1):
            directions.append((dy, -1))

    return directions


def reconstruct(came_from, start, goal):
    """
    Reconstruct the path from goal back to start.
    """
    path = [goal]
    cur = goal
    while cur != start:
        cur = came_from[cur]
        path.append(cur)
    return path[::-1]


def expand_path(path, grid):
    """
    Expand jump points into the full step-by-step path by filling in intermediate tiles.
    """
    if not path:
        return None

    expanded = [path[0]]

    for i in range(1, len(path)):
        y1, x1 = path[i - 1]
        y2, x2 = path[i]

        dy = y2 - y1
        dx = x2 - x1

        sy = 0 if dy == 0 else dy // abs(dy)
        sx = 0 if dx == 0 else dx // abs(dx)

        y, x = y1, x1

        while (y != y2 or x != x2):
            if y != y2:
                y += sy
            if x != x2:
                x += sx

            if not passable(grid, y, x):
                return None
            expanded.append((y, x))

    return expanded


def find_path(start, goal, grid):
    """
    Find the shortest path using JPS algorithm.

    Returns:
    list of tuple: Full expanded path from start to goal,
    or None if no path exists.
    """
    if start == goal:
        return [start]

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))

    came_from = {}
    g_score = {start: 0}
    parent = {start: None}
    closed = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in closed:
            continue
        closed.add(current)

        if current == goal:
            raw = reconstruct(came_from, start, goal)
            return expand_path(raw, grid)

        for dy, dx in prune_neighbors(grid, current, parent[current]):
            jp = jump(grid, current[0], current[1], dy, dx, goal)
            if jp is None or jp in closed:
                continue

            ddy = abs(jp[0] - current[0])
            ddx = abs(jp[1] - current[1])
            diag = min(ddy, ddx)
            straight = max(ddy, ddx) - diag
            cost = diag * math.sqrt(2) + straight

            t = g_score[current] + cost
            if t < g_score.get(jp, float("inf")):
                came_from[jp] = current
                parent[jp] = current
                g_score[jp] = t
                heapq.heappush(open_set, (t + heuristic(jp, goal), jp))
    return None


def find_path_jump_points(start, goal, grid):
    """
    Same as find_path, but returns ONLY jump points (for unit tests).
    """
    if start==goal:
        return [start]

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))

    came_from = {}
    g_score = {start: 0}
    parent = {start: None}
    closed = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current in closed:
            continue
        closed.add(current)

        if current == goal:
            return reconstruct(came_from, start, goal)

        for dy, dx in prune_neighbors(grid, current, parent[current]):
            jp = jump(grid, current[0], current[1], dy, dx, goal)

            if jp is None or jp in closed:
                continue

            ddy = abs(jp[0]-current[0])
            ddx = abs(jp[1]-current[1])
            diag = min(ddy, ddx)
            straight = max(ddy, ddx) - diag
            cost = diag * math.sqrt(2) + straight

            t = g_score[current] + cost

            if t < g_score.get(jp, float("inf")):
                came_from[jp] = current
                parent[jp] = current
                g_score[jp] = t
                heapq.heappush(open_set, (t + heuristic(jp, goal), jp))

    return None
