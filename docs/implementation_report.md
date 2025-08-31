# Implementation Report

## Program Structure

The application is a command-line pathfinding tool that compares two algorithms: **A\*** and **Jump Point Search (JPS)**. The user can choose a default grid or input a custom grid and specify start and goal points. The program then calculates the shortest path using both algorithms. Finally, it prints the grid with the path, the number of steps, and the computation time.

The main program `main.py` handles user input via terminal, grid printing, and initiating the running of the algorithms. The algorithms are implemented in separate files: `a_star.py` and `jps.py`.

## Time Complexity and Performance

- **A\***:  
  - Explores neighbors in four directions (up, down, left, right).  
  - **Time Complexity:** O(b^d) in the worst case, where b is the branching factor (max 4) and d is the depth of the shortest path.  
  - **Space Complexity:** O(b^d) for storing open nodes.  

- **Jump Point Search (JPS):**  
  - Optimizes A* by pruning unnecessary nodes and allowing diagonal movement.  
  - **Time Complexity:** O(b^d) worst case, but typically faster than A* in practice due to reduced node expansions.  
  - **Space Complexity:** O(b^d), similar to A*.  

Performance is measured in single-run execution time. Theoretically, on small grids, both algorithms are fast. However, on larger grids JPS outperforms A* due to pruning.

## Input and Usability

- Coordinates must be within grid bounds.  
- Start and goal points cannot be walls.  
- Custom grid input only accepts `0` (walkable) and `1` (wall).  
If invalid input is provided, a descriptive error message is shown without crashing the program.

The application runs entirely in the terminal and provides clear instructions and grid visualization using ASCII characters (`.`, `█`, and `•` for the path).

## Suggestions for Improvement
 
- Consider adding diagonal movement to A*.  
- Implement visualization & better UI in general.
- Optimize JPS further.

## Use of Large Language Models

- This project used large langue models for help in formatting of .md files.

## Sources

- Russell, Stuart J., and Peter Norvig. *Artificial Intelligence: A Modern Approach*. 4th edition. Pearson, 2020.  
- GeeksforGeeks. "A* Search Algorithm." [https://www.geeksforgeeks.org/dsa/a-search-algorithm/](https://www.geeksforgeeks.org/dsa/a-search-algorithm/)
- GeeksforGeeks. "Introduction to Jump Point Search (JPS)." [https://www.geeksforgeeks.org/advance-java/introduction-to-jsp/](https://www.geeksforgeeks.org/advance-java/introduction-to-jsp/)
