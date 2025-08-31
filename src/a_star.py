from heapq import heappush, heappop

def heuristic(a, b):
    """
    Calculate the Manhattan distance between two points.

    Parameters:
    a (tuple): Coordinates of the first point (row, col).
    b (tuple): Coordinates of the second point (row, col).

    Returns:
    int: Manhattan distance between points a and b.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(grid, node):
    """
    Get all neighbors (walkable) (up, down, left, right) of a given node in the grid.

    Parameters:
    grid (list of list of int): 2D grid representing the map (0 = walkable, 1 = wall).
    node (tuple): Current node coordinates (row, col).

    Returns:
    list of tuple: List of coordinates for all valid neighboring nodes.
    """
    x, y = node
    neighbors = []
    #          up      down    left     right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy

        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def find_path(start, goal, grid):
    """
    Find the shortest path from start to goal using the A* algorithm.

    Parameters:
    start (tuple): Starting coordinates (row, col).
    goal (tuple): Goal coordinates (row, col).
    grid (list of list of int): 2D grid representing the map (0 = walkable, 1 = wall).

    Returns:
    list of tuple: Ordered list of coordinates representing the shortest path from start to goal.
                   Returns an empty list if no path exists.
    """
    open_set = []
    heappush(open_set, (heuristic(start, goal), start))
    came_from = {}  # each node mapped to its parent
    cost_so_far = {start: 0}  # cost from start to each node

    while open_set:
        _, current = heappop(open_set)

        # goal reached so reconstruct path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # return path from start to goal

        # explore neighbors
        for neighbor in get_neighbors(grid, current):
            new_cost = cost_so_far[current] + 1
            if new_cost < cost_so_far.get(neighbor, float("inf")):
                came_from[neighbor] = current
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heappush(open_set, (priority, neighbor))

    # No path found
    return []
