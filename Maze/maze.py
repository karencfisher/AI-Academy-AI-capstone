# to load data files
import csv
# for command line arguments
import sys

# import my search implementations
from searches import depth_first, a_star


class Maze:
    def __init__(self):
        self.maze = None
        self.start = (0, 0)
        pass

    def __str__(self):
        '''
        Provide a printable string version of the maze
        input: none
        return: formatted string
        '''
        assert self.maze is not None, 'Load a maze first!'
        output=[]
        for row in self.maze:
            string = [' ']
            for col in row:
                string.append(col)
            string.append(' ')
            output.append(' | '.join(string))
        return '\n'.join(output)

    def load_maze(self, file_path):
        '''
        Read the CSV file and load the maze from it. Get
        width and height.
        input: CSV file path
        '''
        self.maze = []
        with open(file_path, 'r') as FP:
            reader = csv.reader(FP, delimiter=',')
            for y, row in enumerate(reader):
                self.maze.append(row)

                # check for goal node, if so cache it as self.goal. Needed
                # for A*.
                for x in range(len(row)):
                    if row[x] == 'G':
                        self.goal = (y, x)

        self.height = len(self.maze)
        self.width = len(self.maze[0])

    def get_adjacent(self, cell):
        '''
        Get next squares that can be moved to. 
        Input: cell, tuple containing (y, x) row and column indexes
        returns: list of cells that can traversed to
        '''
        y, x = cell
        jump = int(self.maze[y][x])
        adjacent = []
        if x - jump >= 0:
            adjacent.append((y, x - jump))
        if y - jump >= 0:
            adjacent.append((y - jump, x))
        if x + jump < self.width:
            adjacent.append((y, x + jump))
        if y + jump < self.height:
            adjacent.append((y + jump, x))
        return adjacent

    def solve_maze(self, search_method, verbose):
        '''
        Solve the maze by method
        input: search_method, string {'DFS', 'A*'}
        return: path found
        '''
        assert self.maze is not None, 'First load a maze file!'
        if search_method == 'DFS':
            result = depth_first(self)
        elif search_method == 'A*':
            result = a_star(self, verbose)
        else:
            raise ValueError('Invalid search method')
        return result


def main():
    # Get comman line argument if verbose mode chosen
    if len(sys.argv) > 1:
        verbose = sys.argv[1] == 'verbose'
    else:
        verbose = False

    maze_files = ['4x4Maze-maze.txt', '6x6Maze.txt']
    solution_files = ['4x4Maze-solution.txt', '6x6Maze-solution.txt']
    maze = Maze()
    for maze_file, solution_file in zip(maze_files, solution_files):

        # fetch solution
        solution = []
        with open(solution_file, 'r') as FP:
            reader = csv.reader(FP, delimiter=',')
            for row in reader:
                values = [int(x) for x in row]
                solution.append(tuple(values))

        # implement the Maze object
        maze.load_maze(maze_file)
        print(f'\n{maze}\n')

        # use each search method on it
        for method in ['DFS', 'A*']:
            if verbose:
                print(f'\nPerforming {method} search...')
            result = maze.solve_maze(method, verbose=verbose)
            str_result = [str(r) for r in result]
            print(f'{method}: {"->".join(str_result)}\n')

            # if A* method, see if it matches the expected solution
            if method == 'A*':
                valid = result == solution
                print(f'A* path as expected: {valid}')

if __name__ == '__main__':
    main()
