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
  start = problem.getStartState()
  graph = {}
  graph[start] = problem.getSuccessors(start)
  frontier = util.Stack()
  frontier.push((start,[start]))
  explored = set()

  while frontier:
    (node, path) = frontier.pop()
    explored.update(path)
    for successor in [child[0] for child in problem.getSuccessors(node)if child[0] not in explored]:
        if problem.isGoalState(successor):
            return actions(graph, path + [successor])
        else:
            frontier.push((successor, path + [successor]))
            if successor not in graph:
                graph[successor] = problem.getSuccessors(successor)