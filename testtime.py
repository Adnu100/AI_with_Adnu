import sys
import numpy as np
import matplotlib.pyplot as plt
from timeit import repeat as rep
from algorithms import *
from algorithms.utilities.maze import get_maze

##########################################################
                                                        ##
# NOTE: change this if any more algorithm is            ##
#       added or wanted to be removed                   ##
#       (must comment the below part which overwrites   ##
#        these 2 variables)                             ##
                                                        ##
algorithms = (                                          ## 
    simple,                                             ##
    simulatedannealing,                                 ##
    steepestascent,                                     ##
    astar                                               ##
)                                                       ##
ticklables = [                                          ##
    'simple',                                           ##
    'steepest\nascent',                                 ##
    'simulated\nannealing',                             ##
    'A* algorithm'                                      ##
]                                                       ##
                                                        ##
##########################################################

# To compare all the algorithms available, use this, otherwise comment this
algorithms = tuple(all_list)
ticklables = tuple(i.name for i in algorithms)

def check_running_time(fun, maze, reptimes = 500):
    '''returns the average running time of fun(maze) after trial number of runs (reptimes)'''
    def check_func():
        fun(maze)
    tests = rep(check_func, number = 1, repeat = reptimes)
    return np.mean(tests) * 1000

def check_maze(maze):
    '''checks the running time of all algorithms to solve the maze 'maze'
    yields running time for each algorithm'''
    global algorithms
    for module in algorithms:
        yield check_running_time(module.RUN, maze)

def main(mazes):
    '''takes input as a list of filenames as mazes, converts them to maze.maze_t type and checks 
    the time for solving maze for each available algorithm
    returns a list containing the list of average running time for each maze for an algorithm'''
    times = []
    mazes = [get_maze(filename) for filename in mazes]
    while None in mazes:
        mazes.remove(None)
    for maze in mazes:
        times.append(list(check_maze(maze)))
    return times

def Colors():
    '''infinite alternating RGB colors for bars'''
    while True:
        yield 'r'
        yield 'g'
        yield 'b'

def BarGraph(data):
    '''plots a bar graph obtained by the given data'''
    global ticklables
    fig = plt.figure()
    subfig = fig.add_subplot(111)
    colors = Colors()
    indices = np.arange(0, len(ticklables))
    rects = []
    width = 0.90 / len(data)
    c = - (len(data) / 2)
    for i in data:
        rects.append(subfig.bar(indices + width * c, i, width, color = next(colors)))
        c += 1
    subfig.set_ylabel("running time (miliseconds)")
    subfig.set_xlabel("algorithms")
    subfig.set_xticks(indices - width / 2)
    subfig.set_xticklabels(tuple(ticklables))
    plt.show()

def ask():
    global ticklables
    for i in range(len(ticklables)):
        if input("include %s? : " %ticklables[i]) == "y":
            yield i

def ask_n_add():
    global algorithms, ticklables
    a = list(ask())
    algorithms = [algorithms[i] for i in a]
    ticklables = [ticklables[i] for i in a]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit()
    if "-a" in sys.argv:
        ask_n_add()
    BarGraph(np.array(main(sys.argv[1:])))

