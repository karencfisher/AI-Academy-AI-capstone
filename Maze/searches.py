# to implement priority queue for A*
from heapq import heappop, heappush


def depth_first(maze, v=None):
    '''
    Recursive depth first search
    input: maze. the maze to be searched (as Maze object)
           v, 'verbose' (ignored here)
    returns: the path found
    '''
    path_found = []

    def recurse(node, path):
        '''
        Embedded function to perform recursion        
        '''
        nonlocal path_found
        path.append(node)
        y, x = node

        # goal found?
        if maze.maze[y][x] == 'G':
            path_found = path[:]
            return

        # Get next squares to visit
        adjacent = maze.get_adjacent(node)
        for adj in adjacent:
            if adj in path:
                continue
            recurse(adj, path)
            if len(path) > 0:
                path.pop()

    # run the embedded function
    recurse(maze.start, [])
    return path_found

def retrace_path(parents, end):
    '''
    Helper function for A*. Trace back the path to the
    goal.
    input: parents, dictionary mapping nodes to parents.
           None if start node.
           end: the goal node as tuple (y, x)
    return: path, list of nodes
    '''
    path = []
    path.append(end)
    while parents[end] is not None:
        path.append(parents[end])
        end = parents[end]
    path.reverse()
    return path

def a_star(maze, verbose=False):
    '''
    A* search
    input: maze, the Maze object
           v, verbose. True to print each expanded node with f_score.
    '''
    # keep track of each node's predecessor
    parents = {maze.start: None}

    # the visited nodes are as a dictionary instead of a set so
    # each seen node can be associated with its distance from the
    # start node
    visited = {maze.start: 0}

    # Each node is represented as a tuple, (f_score, (y, x)). This way
    # the priority queue keeps them in sorted order
    que = [(0, maze.start)]
    while len(que) > 0:
        node = heappop(que)
        y, x = node[1]

        # goal found?
        if maze.maze[y][x] == 'G':
            path = retrace_path(parents, node[1])
            break

        # Get next squares to visit
        adjacent = maze.get_adjacent(node[1])
        for adj in adjacent:

            # get summed actual distance to the next node. Distance between squares
            # is 1, so distance is the number of squares jumped to.
            g = visited[node[1]] + int(maze.maze[y][x])

            # if we have not yet visited this node, or we now have a shorter
            # path to it, add it to the queue
            g_adj = visited.get(adj)
            if g_adj is None or g < g_adj:
                if verbose:
                    print(f'Node expanded: {adj} cost: {g}')
                parents[adj] = node[1]
                visited[adj] = g

                # Manhattan distance as heurisitic
                h = abs(adj[0] - maze.goal[0]) + abs(adj[1] - maze.goal[1])
                f = h + g

                heappush(que, (f, adj))
    return path
