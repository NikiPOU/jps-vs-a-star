# User Guide

This program compares two pathfinding algorithms:  
- **A*** (A-star search)  
- **JPS** (Jump Point Search)  

It finds the shortest path from a start point to a goal point on a grid, then displays:  
- The path taken
- The number of steps in the path  
- The time taken to compute the path  

---

## Requirements
- Python 3.8 or later  
- [Poetry](https://python-poetry.org/) for dependency management  

---

## How to Run
From the project root directory, run:

```bash
poetry install        # install dependencies
poetry run python src/main.py

```
## Use Instructions
When you start the program, a short explanation of how it works will be provided and then be prompted for input.

### 1. Choose a grid

Program: 
Use default grid? (yes/no):

- yes: the program will use a deafault 3x3 grid.
E.g.
```text
. . .
█ █ .
. . .
```
- no: enter custom grid line by line.
-- 0 for walkable spaces.
-- 1 for walls.
E.g.
```text
0 0 0 0   . . . .
1 1 0 1 = █ █ . █
0 0 0 0   . . . .
0 1 0 0   . █ . .
```
### 2. Choose star and goal points

Program: 
Enter start point (row col):
Enter goal point (row col):

-Input two integers separated by a space, e.g. 0 0 for the top-left corner.
-You cannot choose a wall (1) as a start or goal point.

### 3. See results

For each algorithm, the program will display:

- The path visualized on the grid:
```text
• = path
█ = wall
. = walkable cell
```

- The number of steps in the path

- The time taken to compute the path


