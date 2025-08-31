# Testing Report

## Unit Testing

Unit tests were written using pytest for both the A* and JPS algorithms. The tests cover:

- Correct pathfinding from a start to a goal point.
- Verification that the path begins and ends at the correct coordinates.
- Validation that the path only moves through walkable cells.
- Consistency of path cost between A* and JPS for the same grid.

## Test Coverage

- An automated unit test: test_simple_path in tests/test_pathfinding.py.
- The test checks a 3x3 grid with a simple obstacle layout.
- Passed successfully.

## Test Inputs and Results

- Test Case 1 - 3x3 Grid:
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

- Test Case 2 - 5x5 Grid:
 ```text
0 0 0 0 0
1 1 0 1 0
0 0 0 1 0
1 1 0 1 0
0 0 0 0 0
 ```
- Start: (0,0)
- Goal: (4,4)

- A* path: valid.
- JPS path: valid.
- Path costs equal.
- Test outcome: Passed

- Test Case 3 - 5x5 Grid with blockage:
 ```text
0 1 0 0 0
1 1 0 1 0
0 0 0 1 0
1 1 0 1 0
0 0 0 0 0
 ```
- Start: (0,0)
- Goal: (4,4)
  
- A* failed to find a path: IndexError in test
- JPS also failed.
- Test outcome: Failed

## Overall Test Results

- A* and JPS successfully found valid paths.
- Path cost was equal for both algorithms.
- Test passed: 2/3 (1/3 failed)
---

## Testing Instructions

 ```code
poetry run pytest --html=report.html --self-contained-html
 ```

