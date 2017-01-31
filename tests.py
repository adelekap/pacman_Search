def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    start = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push((start,[start]),0)
    graph = {}
    graph[start] = problem.getSuccessors(start)
    explored =set()

    while frontier:
        (node,path) = frontier.pop()
        if problem.isGoalState(node):
            return actions(graph, path)
        explored.update(path)
        successors = problem.getSuccessors(node)
        for successor in [child[0] for child in successors if child[0] not in explored]:
            g = problem.getCostOfActions(actions(graph,path+[successor]))
            if successor in (x[1][0] for x in frontier.heap):
                checkCost(frontier,successor,g)
            else:
                frontier.push((successor, path + [successor]), g)
            if successor not in graph:
                graph[successor] = problem.getSuccessors(successor)


