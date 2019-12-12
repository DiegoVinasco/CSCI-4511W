from copy import copy
from copy import deepcopy
from math import sqrt

class Problem:
    """A problem is a compilation of functions that dictate how a sliding puzzle search path can operate through
    acceptable states."""

    def __init__(self, initial):
        """Problem class constructor. It can specify the initial state and set a goal based on the initial state. The
        size will be determined by the height of the initial state."""
        self.initial = initial
        self.size = len(initial)

        # initialize goal
        goal = []
        count = 1
        for row in range(self.size):
            new_row = []
            for col in range(self.size):
                new_row.append(count)
                count += 1
            goal.append(new_row)
        goal[self.size - 1][self.size - 1] = 0
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given state. Actions are returned in an iterator to improve
        performance when many actions are available."""
        actions = []
        for row in range(self.size):
            for col in range(self.size):
                if state[row][col] == 0:
                    for n in range(4):
                        new_action = (row, col, n)
                        # Remove invalid actions
                        if self.stateTest(self.result(state, new_action)):
                            actions.append(new_action)
        return iter(actions)

    def result(self, state, action):
        """Return the state that results from executing the given action in the given state. If the action is within
        bounds but would move the empty state out of bounds result will return None."""
        new_state = deepcopy(state)
        # move left
        if action[2] == 0 and action[1] > 0:
            new_state[action[0]][action[1]] = state[action[0]][action[1] - 1]
            new_state[action[0]][action[1] - 1] = 0
        # move up
        elif action[2] == 1 and action[0] > 0:
            new_state[action[0]][action[1]] = state[action[0] - 1][action[1]]
            new_state[action[0] - 1][action[1]] = 0
        # move right
        elif action[2] == 2 and action[1] < self.size - 1:
            new_state[action[0]][action[1]] = state[action[0]][action[1] + 1]
            new_state[action[0]][action[1] + 1] = 0
        # move down
        elif action[2] == 3 and action[0] < self.size - 1:
            new_state[action[0]][action[1]] = state[action[0] + 1][action[1]]
            new_state[action[0] + 1][action[1]] = 0
        else:
            return None
        return new_state

    def goalTest(self, state):
        """Return True if the state matches the goal state."""
        return self.goal == state

    def stateTest(self, state):
        """Return true if state is acceptable. A valid state has every number from 0 to the last tile number, inclusive,
        exactly once."""
        if not state:
            return False
        for n in range(self.size**2):
            found = False
            for row in range(self.size):
                for col in range(self.size):
                    if state[row][col] == n:
                        if not found:
                            found = True
                        elif found:
                            return False
            if not found:
                return False
        return True

    def __str__(self):
        string = ""
        for row in range(len(self.initial)):
            string += "["
            for col in range(len(self.initial)):
                if self.initial[row][col] >= 10:
                    string += " "
                else:
                    string += "  "
                string += str(self.initial[row][col])
            string += " ]\n"
        return string

    def __repr__(self):
        string = ""
        for row in self.initial:
            string += str(row)
        return string

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node that this is a successor of) and to the
    actual state for this node. Includes the action that got us to this state as well as the score for that state
    according to a passed in heuristic heuristic."""

    def __init__(self, state, parent=None, action=None, cost=0):
        """Create a search tree Node, derived from a parent by an action.
        Update the node parameters based on constructor values"""
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        self.cost = cost
        # If depth is specified then depth of node will be 1 more than the depth of parent
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem, heuristic=lambda var1, var2: 0):
        """List the nodes reachable in one step from this node. If no heuristic is passed in the default cost will be
        zero."""
        return [self.child_node(problem, action, heuristic)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action, heuristic):
        """A helper function for expand. The cost function is used to estimate a score for the node according to a
        passed om heuristic."""
        state = problem.result(self.state, action)
        cost = getCost(state, problem.goal, problem.size, heuristic)
        return Node(state, self, action, cost)

    def getPathCost(self):
        cost = self.cost
        node = copy(self)
        while node.parent:
            node = node.parent
            cost += node.cost
        return cost

    def __str__(self):
        string = ""
        for row in range(len(self.state)):
            string += "["
            for col in range(len(self.state)):
                string += str(self.state[row][col])
                if self.state[row][col] < 10:
                    string += " "
            string += "]\n"
        string += "Depth: " + str(self.depth) + "\n"
        string += "Action: " + str(self.action) + "\n"
        string += "Cost: " + str(self.cost) + "\n"
        return string

    def __repr__(self):
        string = ""
        for row in self.state:
            string += str(row)
        return string


class NodePriorityQueue:
    """A priority queue composed of nodes. Priority is assigned by each node's cost and a lower score is valued over a
    larger score."""

    def __init__(self):
        self.queue = []

    def enqueue(self, new_node):
        """Add a new node to the queue then sort it by its cost."""
        self.queue.insert(0, new_node)
        self.queue.sort(key=lambda node: node.cost)

    def dequeue(self):
        """Retrieve the first node from the queue."""
        if not self.empty():
            return self.queue.pop(0)
        return None

    def empty(self):
        """Return whether the queue is empty."""
        return len(self.queue) < 1

    def __str__(self):
        string = ""
        for node in self.queue:
            string += str(node) + "\n"
        return string

    def __repr__(self):
        string = ""
        for node in self.queue:
            string += repr(node) + " "
        return string

### A* functions ###

def getManhattan(var1, var2): # (row, col)
    """Pass in two tuple coordinates and calculate the Manhattan distance between the them."""
    return abs(var1[0] - var2[0]) + abs(var1[1] - var2[1])

def getStraightLine(var1, var2): # (row, col)
    """Pass in two tuple coordinates and calculate the direct distance between the them."""
    return sqrt( (var1[0] - var2[0])**2 + (var1[1] - var2[1])**2 )

def getCost(state, goal, size, heuristic):
    """Use a heuristic to estimate the cost of a node."""
    distance = 0
    for goal_row in range(size):
        for goal_col in range(size):
            if goal[goal_row][goal_col] == 0:
                continue
            found = False
            for node_row in range(size):
                if found:
                    break
                for node_col in range(size):
                    if state[node_row][node_col] == goal[goal_row][goal_col]:
                        distance += heuristic((goal_row, goal_col), (node_row, node_col))
                        found = True
                        break
    return distance


def AStar(problem, heuristic):
    # Start from first node of the problem Tree
    node = Node(problem.initial)
    node.cost = getCost(problem.initial, problem.goal, problem.size, heuristic)
    print("Initial cost:", node.cost)
    # Create a Queue to store all nodes of a particular level and an explored list to track visited nodes.
    frontier = NodePriorityQueue()
    frontier.enqueue(node)
    explored = []
    # Check to make sure initial is not already solved
    if problem.goalTest(node.state):
        print("Problem is already solved\n")
        return node
    # Loop until all nodes are explored (frontier queue is empty) or goalTest's criteria is met
    while not frontier.empty():
        # Remove from frontier, for analysis
        node = frontier.dequeue()
        # Loop over all children of the current node
        for child in node.expand(problem, heuristic):
            # Check against explored set
            found = False
            for visited in explored:
                if visited.cost == child.cost and visited.state == child.state:
                    found = True
                    break
            if found:
                continue
            # If child node meets goalTest's criteria return the path history
            if problem.goalTest(child.state):
                print("Goal state found\n")
                return child
            # Add every new child to the frontier
            frontier.enqueue(child)
        # After expanding a node add it to the explored set
        explored.append(node)
    print("Goal not found\n")
    return None
