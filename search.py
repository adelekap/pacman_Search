# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
import random

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


class Node:
    def __init__(self,state,children,parent=None,depth=None):
        self.State = state
        self.Parent = parent
        self.Children = children
        self.Depth = depth



def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def constructPath(node):
    """
    Returns a list of actions given the goal node (instance of Node class).
    """
    backPath =[]
    while node.Parent != None:
        backPath.append([child[1] for child in node.Parent.Children if child[0] == node.State][0])
        node = node.Parent
    return list(reversed(backPath))


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    start = problem.getStartState()
    frontier = util.Stack()
    frontier.push(Node(start,problem.getSuccessors(start)))
    explored = set()

    while frontier:
        node = frontier.pop()
        if problem.isGoalState(node.State):
            return constructPath(node)
        if node.State not in explored:
            explored.update([node.State])
            for child in node.Children:
                frontier.push(Node(child[0],[suc for suc in problem.getSuccessors(child[0]) if suc[0] not in explored],
                                   node))


def breadthFirstSearch(problem):
    "Search the shallowest nodes in the search tree first. [p 81]"
    start = problem.getStartState()
    frontier = util.Queue()
    frontier.push(Node(start,problem.getSuccessors(start)))
    explored = set()

    while frontier:
        node = frontier.pop()
        if node.State not in explored:
            explored.update([node.State])
            for child in node.Children:
                if problem.isGoalState(child[0]):
                    goal = Node(child[0],None,node)
                    return constructPath(goal)
                frontier.push(Node(child[0],[suc for suc in problem.getSuccessors(child[0]) if suc[0] not in explored],
                                   node))


def checkCost(frontier, value, cost):
    """
    Ensures that node in the frontier does not have a higher path-cost.
    If it does, it will push the node with the lower cost into the queue.
    """
    for x in frontier.heap:
        if x[1][0] == value and cost < x[0]:
            frontier.push(x[1], cost)


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    start = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push(Node(start,problem.getSuccessors(start)),0)
    explored = set()

    while frontier:
        node = frontier.pop()
        if problem.isGoalState(node.State):
            return constructPath(node)
        if node.State not in explored:
            explored.update([node.State])
            for child in node.Children:
                frontier.push(Node(child[0],[suc for suc in problem.getSuccessors(child[0]) if suc[0] not in explored],
                                   node),)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    start = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push((start, [start]), 0)
    graph = {}
    graph[start] = problem.getSuccessors(start)
    explored = set()

    while frontier:
        (node, path) = frontier.pop()
        if problem.isGoalState(node):
            return actions(graph, path)
        explored.update(path)
        if node not in graph:
            successors = problem.getSuccessors(node)
        else:
            successors = graph[node]
        for successor in [child[0] for child in successors if child[0] not in explored]:
            g = problem.getCostOfActions(actions(graph, path + [successor]))
            h = heuristic(successor, problem)
            if successor in (x[1][0] for x in frontier.heap):
                checkCost(frontier, successor, g)
            else:
                frontier.push((successor, path + [successor]), g + h)
            if successor not in graph:
                graph[successor] = problem.getSuccessors(successor)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
