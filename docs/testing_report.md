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

## Test Inputs

- 3x3 grid example:
 ```text
0 0 0
1 1 0
0 0 0
 ```

## Test Results

- A* and JPS successfully found valid paths.
- Path cost was equal for both algorithms.
- Test passed: 1/1
---

## Testing Instructions

 ```code
poetry run pytest --html=report.html --self-contained-html
 ```
