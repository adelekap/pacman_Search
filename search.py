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
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]


def unvisited_nodes(successors, visitedNodes):
    """
    Returns a list of the un-visited nodes from a list of possible nodes.
    """
    unvisited = []
    for node in successors:
        if node[0] not in visitedNodes:
            unvisited.append(node[0])
    return unvisited


# def shortest_path(paths):
#     """
#     Returns the shortest path of coordinates given a list of
#     possible paths to reach the goal state.
#     """
#     lengths = []
#     for path in paths:
#         lengths.append(len(path))
#     best = paths[lengths.index(min(lengths))]
#     return best


def actions(graph,positions):
    """
    Returns the sequence of actions an agent
    """
    actions = []
    for i in range(len(positions)-1):
        posDest = graph[positions[i]]
        for dest in posDest:
            if dest[0] == positions[i+1]:
                actions.append(dest[1])
    return actions


def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """

  start = problem.getStartState()
  graph = {}
  graph[start] = problem.getSuccessors(problem.getStartState())
  frontier = util.Stack()
  frontier.push((start,[start]))
  explored = set()

  while frontier:
    (node, path) = frontier.pop()
    explored.update(path)
    for successor in unvisited_nodes(graph[node],explored):
        if problem.isGoalState(successor):
            return actions(graph, path + [successor])
        else:
            frontier.push((successor, path + [successor]))
            if successor not in graph:
                graph[successor] = problem.getSuccessors(successor)


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  start = problem.getStartState()
  graph = {}
  graph[start] = problem.getSuccessors(problem.getStartState())
  frontier = util.Queue()
  frontier.push((start,[start]))
  explored = set()

  while frontier:
    (node, path) = frontier.pop()
    explored.update(path)
    for successor in unvisited_nodes(graph[node], explored):
        if problem.isGoalState(successor):
            return actions(graph, path + [successor])
        else:
            frontier.push((successor, path + [successor]))
            if successor not in graph:
                graph[successor] = problem.getSuccessors(successor)

def getCost(graph, position, destination):
    """
    Returns the cost of an action given the expanded environment, current position,
    and destination after action has been executed.
    """
    for pos in graph[position]:
        if pos[0] == destination:
            return pos[2]


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    start = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push((start,[start]),0)
    graph = {}
    graph[start] = problem.getSuccessors(problem.getStartState())
    explored =set()

    while frontier:
        (node,path) = frontier.pop()
        explored.update(path)
        for successor in unvisited_nodes(graph[node], explored):
            if problem.isGoalState(successor):
                return actions(graph, path +[successor])
            else:
                frontier.push((successor, path + [successor]), getCost(graph, path[-1],successor))
                if successor not in graph:
                    graph[successor] = problem.getSuccessors(successor)


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
    frontier.push((start,[start]),0)
    graph = {}
    graph[start] = problem.getSuccessors(problem.getStartState())
    explored = set()

    while frontier:
        (node,path) = frontier.pop()
        explored.update(path)
        for successor in unvisited_nodes(graph[node], explored):
            if problem.isGoalState(successor):
                return actions(graph, path +[successor])
            else:
                g = getCost(graph,path[-1],successor)
                h = heuristic(successor,problem)
                frontier.push((successor,path + [successor]), (g + h))
                if successor not in graph:
                    graph[successor] = problem.getSuccessors(successor)
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch