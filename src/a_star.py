from heapq import heappush, heappop

def heuristic(a, b):
    #manhattan dist in grid (no daigonals)
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def get_neighbors(grid, node):
    x,y = node
    neighbors=[]
    moves = [(-1,0), (1,0), (0,-1), (0,1)]
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny]==0:
            neighbors.append((nx, ny))
    return neighbors

def find_path(start, goal, grid):
    open_set=[]
    heappush(open_set, (0 + heuristic(start, goal), 0, start))
    came_from= {}
    g_score = {start: 0} #sortest known distance to each node from start

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

        for neighbor in get_neighbors(grid, current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heappush(open_set, (f_score, tentative_g_score, neighbor))
    return []
