import SlidingPuzzle as main
from datetime import datetime
from random import randint

def runTest(problem):
    # Given a problem this will run both the manhattan and straight line tests are print
    print("Initial State:")
    print(problem)
    print("\nRunning Manhattan Test")
    start_time = datetime.now()
    manhattan_result = main.AStar(problem, lambda var1, var2: main.getManhattan(var1, var2))
    manhattan_time = datetime.now() - start_time
    print("Running StraightLine Test")
    start_time = datetime.now()
    straight_result = main.AStar(problem, lambda var1, var2: main.getStraightLine(var1, var2))
    straight_time = datetime.now() - start_time
    print("--- Results ---\n")
    print("Manhattan Time:", manhattan_time)
    print("Manhattan Cost:", manhattan_result.getPathCost())
    print("Manhattan Depth:", manhattan_result.depth)
    print("Straight-Line Time:", straight_time)
    print("Straight-Line Cost:", straight_result.getPathCost())
    print("Straight-Line Depth:", straight_result.depth, "\n")

def generateProblem(size, complexity=0):
    # Create a random puzzle of a given size. Use complexity to choose the number of changes made to the board
    initial = []
    count = 1
    for x in range(size):
        row = []
        for y in range(size):
            row.append(count)
            count += 1
        initial.append(row)
    initial[size - 1][size - 1] = 0
    # mix up node by complexity
    problem = main.Problem(initial)
    node = main.Node(initial)
    while complexity > 0:
        max = 0
        for action in node.expand(problem, lambda var1, var2: randint(0, 3)):
            if action.cost > max:
                node = action
                max = action.cost
        complexity -= 1
    return main.Problem(node.state)

### Initialize problems and tests ###

test1 = [[1,2,3],
         [4,5,6],
         [7,0,8]]

test2 = [[8,3,2],

         [7,4,6],
         [5,1,0]]

### Run tests ###
# print("=== Initial goal test ===\n")
# problem = generateProblem(3)
# runTest(problem)
# print("=== Near solution test ===\n")
# problem = main.Problem(test1)
# runTest(problem)
# print("=== Static 3x3 test ===\n")
# problem = main.Problem(test2)
# runTest(problem)
#
# Read, generate, and run random tests
# for i in range(1000):
#     print("=== Random 4x4 test " + str(i) + " ===\n")
#     problem = generateProblem(4, i)
#     runTest(problem)


class experiment:
    def __init__(self, complexity, m_init, m_time, m_cost, m_depth, s_init, s_time, s_cost, s_depth):
        self.comp = complexity
        self.minit = m_init
        self.mtime = m_time
        self.mcost = m_cost
        self.mdepth = m_depth
        self.sinit = s_init
        self.stime = s_time
        self.scost = s_cost
        self.sdepth = s_depth

results = []
complexity = 0
f = open("compres.txt", 'r')

while complexity < 500:
    line = f.readline()
    while not '===' in line:
        line = f.readline()
    while not 'Initial cost' in line:
        line = f.readline()
    m_init = line[14:].strip()
    line = f.readline()
    while not 'Initial cost' in line:
        line = f.readline()
    s_init = line[14:].strip()
    line = f.readline()
    while not 'Manhattan' in line:
        line = f.readline()
    m_time = line[16:].strip()
    line = f.readline()
    m_cost = line[16:].strip()
    line = f.readline()
    m_depth = line[17:].strip()
    line = f.readline()
    s_time = line[20:].strip()
    line = f.readline()
    s_cost = line[20:].strip()
    line = f.readline()
    s_depth = line[21:].strip()
    result = experiment(complexity, m_init, m_time, m_cost, m_depth, s_init, s_time, s_cost, s_depth)
    results.append(result)
    complexity += 1

f = open("results.txt", 'w')

for r in results:
    line = str(r.comp) + " " + str(r.minit) + " " + str(r.mcost) + " " + str(r.mtime) + " " + str(r.mdepth) + " " + str(r.sinit) + " " + str(r.scost) + " " + str(r.stime) + " " + str(r.sdepth) + " "
    f.write(line + '\n')