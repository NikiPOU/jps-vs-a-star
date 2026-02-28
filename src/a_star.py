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
    Check if moving to a new position allowed.

    Parameters:
    grid (list of list of int): 2D grid
    y, x (int): Current position
    ny, nx (int): New position

    Returns:
    bool: True if the move is valid.
    """
    return passable(grid,ny,nx)


def heuristic(a, b):
    """
    Calculate the Octile distance between two points.
    """
    dy = abs(a[0]-b[0])
    dx = abs(a[1]-b[1])
    return max(dx, dy) + (math.sqrt(2)-1) * min(dx, dy)


def find_path(start, goal, grid):
    """
    Find shortest path from start to goal using the A*.

    Movement allows 8 directions.
    Straight moves cost 1
    Diagonal moves cost sqrt(2)

    Returns:
    list of tuple: Ordered list of coordinates from start to goal.
    Returns None if no path exists.
    """
    if start == goal:
        return [start]

    open_heap = []
    heapq.heappush(open_heap, (0,start))

    came_from = {}
    g_score = {start: 0}

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        y,x = current

        for dy, dx in [
            (-1,0), (1,0), (0,-1), (0,1),
            (-1,-1), (-1,1), (1,-1), (1,1)
        ]:
            ny = y+dy
            nx = x+dx

            if not valid_move(grid,y,x,ny,nx):
                continue

            step_cost = math.sqrt(2) if dy != 0 and dx != 0 else 1
            t = g_score[current] + step_cost

            if t < g_score.get((ny, nx), float("inf")):
                came_from[(ny,nx)] = current
                g_score[(ny,nx)] = t
                f = t + heuristic((ny,nx), goal)
                heapq.heappush(open_heap, (f, (ny,nx)))

    return None
