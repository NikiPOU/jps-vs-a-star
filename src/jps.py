def is_passable(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

def jump(grid, x, y, dx, dy, goal):

    nx, ny = x + dx, y + dy

    if not is_passable(grid, nx, ny):
        return None

    if (nx, ny) == goal:
        return (nx, ny)

    if dx != 0 and dy != 0:

        if (not is_passable(grid, nx - dx, ny) or not is_passable(grid, nx, ny - dy)):
            return None

        if jump(grid, nx, ny, dx, 0, goal) is not None or jump(grid, nx, ny, 0, dy, goal) is not None:
            return (nx, ny)

    if dx != 0 and dy == 0:

        if (is_passable(grid, nx, ny+1) and not is_passable(grid, x, y+1)) or \
           (is_passable(grid, nx, ny-1) and not is_passable(grid, x, y-1)):
            return (nx, ny)

    elif dy != 0 and dx == 0:

        if (is_passable(grid, nx+1, ny) and not is_passable(grid, x+1, y)) or \
           (is_passable(grid, nx-1, ny) and not is_passable(grid, x-1, y)):
            return (nx, ny)

    return jump(grid, nx, ny, dx, dy, goal)


def get_successors(grid, node, goal):
    x, y = node
    successors = []
    directions = [
        (-1,0), (1,0), (0,-1), (0,1),
        (-1,-1), (-1,1), (1,-1), (1,1)
    ]
    for dx, dy in directions:
        jp = jump(grid, x, y, dx, dy, goal)
        if jp is not None:
            successors.append(jp)
    return successors


from heapq import heappush, heappop

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def find_path(start, goal, grid):
    open_set = []
    heappush(open_set, (heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, cost, current = heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in get_successors(grid, current, goal):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heappush(open_set, (f_score, tentative_g_score, neighbor))
    return []
