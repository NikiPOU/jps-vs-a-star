# Testing Report

## Unit Testing

Unit tests were written using pytest for both the A* and JPS algorithms. The tests cover:

- Correct pathfinding from a start to a goal point.
- Verification that the path begins and ends at the correct coordinates.
- Validation that the path only moves through walkable cells.
- Consistency of path cost between A* and JPS for the same grid.
- Performance benchmarking on larger grids.

## Test Coverage

- test_simple_path: 3x3 grid, simple obstacle layout.
- test_no_path: 3x3 grid with impossible path.
- test_start_equals_goal: 2x2 grid where start == goal.
- test_larger_open_grid: 10x10 grid with obstacles.
- test_performance_a_star & test_performance_jps: 50x50 grids with obstacles for measuring runtime.

## Test Inputs and Results

Test Case 1 - 3x3 Grid:
 ```text
0 0 0
1 1 0
0 0 0
 ```
- Start: (0,0)
- Goal: (2,2)

Results:
- A* path: valid.
- JPS path: valid.
- Path costs equal.
- Test outcome: Passed

Test Case 2 - No possible path:
 ```text
0 1 0
1 1 1
0 1 0
 ```
- Start: (0,0)
- Goal: (2,2)

- A* path: None.
- JPS path: None.
- Test outcome: Passed.

Test Case 3 - Start == Goal:
 ```text
0 0
0 0
 ```
- Start: (1,1)
- Goal: (1,1)

- Test outcome: Passed.

Test Case 4 - Large 10x10 Grid with obstacles:
 ```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
 ```
- Start: (0,0)
- Goal: (9,9)
  
- A* path: valid.
- JPS path: valid.
- Test outcome: Passed.

Test Case 5 - Performance 50x50:

- Start: (0,0)
- Goal: (49,49)
  
- A* runtime: approx. 0.0053s
- JPS runtime: approx. 0.0087s
- Test outcome: Both paths valid.

## Overall Test Results

- 6 executed unit tests.
- 6/6 passed.
---

## Testing Instructions

 ```code
poetry run pytest --html=report.html --self-contained-html
 ```



