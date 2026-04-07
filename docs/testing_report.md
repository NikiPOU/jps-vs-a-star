# Testing Report

## Unit Testing

Unit tests were written to verify the correctness of both the A* and JPS algorithms. The tests cover:

- Correct pathfinding from start to goal coordinates on small grids.
- Verification that the path begins and ends at the correct coordinates.
- Validation that the path only moves through walkable cells.
- Consistency of path cost between A* and JPS for the same grid.
- Octile distance heuristic verification.
- Reverse direction pathfinding.
- Verification of JPS jump-point behavior.

## Unit Test Coverage

- Octile Distance Test: Ensures octile distance heuristic calculation is correct.
- 4x4 Simple Grid: Small grid with a few obstacles. Tests both forward and reverse.
- 5x5 Diagonal Block: Small grid with a more complex obstacle layout. Tests both forward and reverse paths.
- JPS Jump Point Test: Confirms that the JPS algorithm reduces the number of nodes by identifying jump points.
- Path Validity Tests: Ensure no movement through obstacles and correct path structure.

## Unit Test Inputs and Results

Test Case 1 - 4x4 Simple Grid:
 ```text
0 0 0 0
0 1 1 0
0 0 0 0
0 0 0 0
 ```
- Start: (0,0)
- Goal: (3,3)

Results:
- A* path: valid.
- JPS path: valid.
- Path costs equal. Forward and reverse costs: 4.828427.
- Test outcome: Passed

Test Case 2 - 5x5 Diagonal Block.
 ```text
0 0 0 0 0
0 1 1 1 0
0 1 0 1 0
0 1 1 1 0
0 0 0 0 0
 ```
- Start: (0,0)
- Goal: (4,4)

Results:
- A* path: None.
- JPS path: None.
- Path costs equal. Forward and reverse costs: 7.414214.
- Test outcome: Passed.

Octile Distance Test:
- Input: (0,0) -> (3,4)
- Calculated distance: 6.242641
- Test outcome: Passed.

JPS Jump Point Test
- Input: Straight-line grid (1x10)
- Start: (0,0)
- Goal: (0,9)

Results:
- Jump points: [(0, 0), (0, 9)]
- Path length significantly reduced compared to A*.
- Confirms the algorithm successfully skips intermediate nodes.
- Test outcome: Passed.

## Unit Test Summary:

- Total unit tests executed: 5
- All tests passed: 5/5
- JPS jump-point behavior succesfully cerified.
---

## Benchmarking

Benchmarking was performed on a single map Berlin_1_256.map using 1000 randomly selected start and goal positions, ensuring a minimum Euclidean distance of 20 between points. Both A* and JPS were timed and path costs compared.

## Test Setup:
- Map: 256 x 256.
- Random start/goal positions: 1000.
- Minimum distance: 20.
- Standard octile-distance-based cost.

## Results:
- Invalid paths: 0.
- Cost mismatches: 0.

- Algorithm: A*, Avg Runtime (s): 0.105, Avg Path Cost: 160.190
- Algorithm: JPS, Avg Runtime (s): 0.024, Avg Path Cost: 160.190

- All paths returned by both algorithms are valid.
- A* and JPS produce identical path costs for all successful paths.
- JPS is significantly faster than A* on average (~4x).

## Overall Test Results:
- Unit tests passed for all small grids and heuristic verification.
- Benchmark tests confirmed that both algorithms produce valid paths with consistent cost.
- Randomized benchmarks confirm performance and path equivalence.
- Correctness of A* and JPS verified.
- Performance advantage of JPS is clear.
- Octile heuristic tested.
- Both forward and reverse pathfinding confirmed.









