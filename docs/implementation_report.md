# Requirements Specification

## Study Program
Computer Science, Bachelor’s Degree

## Project Overview
This project is a command-line application comparing two pathfinding algorithms: A* and Jump Point Search (JPS). The program allows users to input a grid map, start and goal points, and then calculate the shortest path using both algorithms. It reports the paths found, step counts, and execution times to showcase performance differences.

The application is implemented in Python. The grid consists of walkable cells and obstacles, and the user interacts via text input in the terminal.

## Technical Requirements
- Compatible with Windows, Linux, and macOS operating systems.
- Requires Python 3.10 or newer.
- Command-line interface.
- Dependency management with Poetry.
- Unit testing with Unittest or pytest.

## Functional Requirements
- User can choose to use a default grid or enter a custom grid (with walkable (0) and blocked (1) cells) via the terminal.
- User inputs start and goal coordinates in (row, column) format.
- Input validation prevents start/goal points on obstacles.
- The program notifies the user of invalid input without crashing.
- Both algorithms find paths, or correctly report when no path exists.
- The grid and resulting paths are printed.
- Performance metrics (steps and time) are shown for both algorithms.
- The codebase supports automated testing,