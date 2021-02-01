import random
import itertools


def add_edge(inputGraph, vertex, vertexTo):
    inputGraph[vertex].append(vertexTo)
    inputGraph[vertexTo].append(vertex)


def add_vertex(inputGraph, vertex):
    inputGraph[vertex] = []


def createRandomGraph(V, E):
    graph = {}
    for i in range(V):
        add_vertex(graph, i)

    for _ in range(E):
        selectRandomIndex = random.randint(0, V - 1)
        while len(graph[selectRandomIndex]) == V - 1:
            selectRandomIndex = random.randint(0, V - 1)
        selectRandomIndex2 = random.randint(0, V - 1)
        while selectRandomIndex2 == selectRandomIndex or selectRandomIndex2 in graph[selectRandomIndex]:
            selectRandomIndex2 = random.randint(0, V - 1)
        add_edge(graph, selectRandomIndex, selectRandomIndex2)
    return graph


def heuristicLongestCycle(graph, V):
    visitedDict = {}
    for vertex in graph:
        visitedDict[vertex] = False

    randomRootNodes = list(range(V))
    isCycle = [False]
    result = []

    while not isCycle[0] and randomRootNodes:
        copyGraph = graph.copy()
        rootVertex = randomRootNodes[random.randint(0, len(randomRootNodes) - 1)]
        Visit(rootVertex, isCycle, randomRootNodes, visitedDict, copyGraph, result)

    result = result[result.index(result[-1]):]

    result = improveCycle(graph, result)

    return result


def improveCycle(graph, result):
    toBeAdded = {}
    for i in range(len(result) - 2):
        neighbourList1 = graph[result[i]]
        neighbourList2 = graph[result[i + 1]]
        sharedNodes = list(set(neighbourList1).intersection(neighbourList2))
        if sharedNodes:
            for sharedNode in sharedNodes:
                if sharedNode not in result:
                    toBeAdded[sharedNode] = i + 1
                    break

    for node in toBeAdded:
        result.insert(toBeAdded[node], node)

    return result


def Visit(v, isCycle, potentialNextRootNodes, visitCheckDict, graph, result):
    visitCheckDict[v] = True
    if not isCycle[0]:
        result.append(v)
    if v in potentialNextRootNodes:
        potentialNextRootNodes.remove(v)

    for neighbour in graph[v]:
        if not visitCheckDict[neighbour]:
            graph[neighbour].remove(v)
            Visit(neighbour, isCycle, potentialNextRootNodes, visitCheckDict, graph, result)
        else:
            if not isCycle[0]:
                result.append(neighbour)
            isCycle[0] = True
            break


def exactLongestCycle(graph, V):
    vertex = list(range(V))
    longestCycle = []
    for size in range(2, V + 1):
        allCombinations = list(itertools.combinations(vertex, size))
        for eachCombination in allCombinations:
            eachCombinationList = list(eachCombination)
            isCycle = True
            for index in range(len(eachCombinationList)):
                nextIndex = index + 1
                if index == len(eachCombinationList) - 1:
                    nextIndex = 0

                currentNode = eachCombinationList[index]
                nextNode = eachCombinationList[nextIndex]
                if nextNode not in graph[currentNode]:
                    isCycle = False
                    break
            if isCycle:
                eachCombinationList.append(eachCombinationList[0])
                longestCycle = eachCombinationList.copy()

    return longestCycle


V, E = 15, 50

graph1 = createRandomGraph(V, E)

print(graph1)

print(exactLongestCycle(graph1, V))
print(heuristicLongestCycle(graph1, V))

