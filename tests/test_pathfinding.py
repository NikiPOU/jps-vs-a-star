import sys
import os

# Add the 'src' directory to sys.path so Python can find your modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from a_star import find_path as a_star_path
from jps import find_path as jps_path

def test_a_star_basic():
    start = (0, 0)
    goal = (1, 1)
    grid = [[0, 0], [0, 0]]
    path = a_star_path(start, goal, grid)
    assert path is not None
    assert path[0] == start
    assert path[-1] == goal

def test_jps_basic():
    start = (0, 0)
    goal = (1, 1)
    grid = [[0, 0], [0, 0]]
    path = jps_path(start, goal, grid)
    assert path is not None
    assert path[0] == start
    assert path[-1] == goal
