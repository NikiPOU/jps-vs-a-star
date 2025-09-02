from heapq import heappush, heappop
import math

def heuristic(a, b):
    """
    Calculate the Octile distance between two points.
    Works well for 8-directional grids (diagonals allowed).
    """
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

def get_neighbors(grid, node):
    """
    Get all 8 neighbors (walkable) of a given node in the grid.

    Parameters:
    grid (list of list of int): 2D grid (0 = walkable, 1 = wall).
    node (tuple): Current node coordinates (row, col).

    Returns:
    list of tuple: List of coordinates for all valid neighboring nodes.
    """
    x, y = node
    neighbors = []
    moves = [
        (-1, 0), (1, 0), (0, -1), (0, 1),        # straight
        (-1, -1), (-1, 1), (1, -1), (1, 1)       # diagonals
    ]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def find_path(start, goal, grid):
    """
    Find the shortest path from start to goal using the A* algorithm with diagonals.

    Returns:
    list of tuple: Ordered list of coordinates representing the shortest path from start to goal.
                   Returns None if no path exists.
    """
    open_set = []
    heappush(open_set, (heuristic(start, goal), start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in get_neighbors(grid, current):
            # cost = 1 for straight, sqrt(2) for diagonal
            step_cost = math.sqrt(2) if (neighbor[0] != current[0] and neighbor[1] != current[1]) else 1
            new_cost = cost_so_far[current] + step_cost

            if new_cost < cost_so_far.get(neighbor, float("inf")):
                came_from[neighbor] = current
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heappush(open_set, (priority, neighbor))

    return None
