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

class Node(object):
    def __init__(self, state, children = [],parent=None, dir = None):
        self.State = state
        self.Parent = parent
        self.Children = children
        self.Dir = dir

    def __iter__(self):
        return (c for c in self.State)

    def __eq__(self, other):
        return self.State == other



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
        backPath.append([child.Dir for child in node.Parent.Children if child.State == node.State][0])
        node = node.Parent
    return list(reversed(backPath))


def cost(node):
    """
    Returns the path cost g(n) given the current node n.
    """
    cost = 0
    while node.Parent != None:
        cost += ([child[2] for child in node.Parent.Children if child[0] == node.State][0])
        node = node.Parent
    return cost


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
    startNode = Node(start)
    startNode.Children = [Node(s[0],parent=startNode, dir=s[1]) for s in problem.getSuccessors(startNode)]
    frontier.push(startNode)
    explored = set()

    while frontier:
        node = frontier.pop()
        if node.State not in explored:
            explored.update([node.State])
            for child in node.Children:
                if problem.isGoalState(child):
                    goal = Node(child.State,parent=node)
                    return constructPath(goal)
                child.Children = [Node(suc[0],parent=child, dir=suc[1]) for suc in problem.getSuccessors(child) if suc[0] not in explored]
                frontier.push(child)




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
                childNode = Node(child[0],[suc for suc in problem.getSuccessors(child[0]) if suc[0] not in explored],
                                   node)
                frontier.push(childNode,cost(childNode))


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
    frontier.push(Node(start,problem.getSuccessors(start)),0)
    explored = set()

    while frontier:
        node = frontier.pop()
        if problem.isGoalState(node.State):
            return constructPath(node)
        if node.State not in explored:
            explored.update([node.State])
            for child in node.Children:
                childNode = Node(child[0],[suc for suc in problem.getSuccessors(child[0]) if suc[0] not in explored],
                                   node)
                g = cost(childNode)
                h = heuristic(child[0], problem)
                frontier.push(childNode,(g + h))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
