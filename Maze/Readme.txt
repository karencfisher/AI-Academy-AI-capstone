The solution is implemented with two Python files:
1) maze.py - The maze itself. It is able to load each example implemented
   one instance of the class.
2) searches.py: implementations of DFS and A* searches

To run both examples from command line:

To run without printing nodes exapnded during A*:

>>python maze.py

To run include printing nodes expanded during A* (verbose mode)

>>python maze.py verbose

You can also load and solve mazes from the Python CLI, Jupyter Notebook, etc. For example,
to use a different test case (as a data file in the same format) then given with the
original problem specification

>>> from maze import Maze
>>> maze = Maze()
>>> maze.load_maze('6x6Maze.txt')
>>> result = maze.solve_maze('A*', True)
Node expanded: (0, 5) cost: 5
Node expanded: (5, 0) cost: 5
Node expanded: (0, 1) cost: 9
Node expanded: (4, 5) cost: 9
Node expanded: (4, 1) cost: 13
Node expanded: (3, 0) cost: 7
...

>>> print(result)
[(0, 0), (0, 5), (4, 5), (4, 1), (1, 1), (1, 4), (3, 4), (5, 4), (2, 4), (2, 0), (1, 0), (1, 3), (5, 3), (5, 5)]

In the maze.solve_maze the parameters are the type of search {'DFS', 'A*'} and the
verbosity (True or False). This use does not validate results against a solution
file however.
