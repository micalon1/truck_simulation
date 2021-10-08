from collections import defaultdict
import heapq as hq


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop()
        else:
            print("pop() error: Stack is empty.")
            return None

    def peek(self):
        if self.items:
            return self.items[-1]
        else:
            print("peek() error: Stack is empty.")
            return None

    def size(self):
        return len(self.items)



#builds adjacency list
    
def build_adjlist(map):
    adj = {}
    for v in map:
        source = v[0]
        destination = v[1]
        if source not in adj:
            adj[source] = []
        adj[source].append(destination)
    for v in map:
        source = v[1]
        destination = v[0]
        if source not in adj:
            adj[source] = []
        adj[source].append(destination)
    for value in adj.values():
        value.sort(key=lambda x: x.lower())
    return adj




def find_path(edges, source, destination):
    status = {}
    adj = build_adjlist(edges)
    for link in edges:
        status[link[0]] = "unvisited"
        status[link[1]] = "unvisited"
    q = Queue()
    q.enqueue([source])
    status[source] = "visiting"
    while not q.isEmpty():
        vertex = q.dequeue()
        if vertex[-1] == destination:
            return vertex
        for n in adj[vertex[-1]]:
            if status[n] != "visited":
                status[n] = "visited"
                q.enqueue(vertex + [n])

"""
BFS
"""

def bfs(map, office):
    path = {}                
    adj = build_adjlist(map)
    for node in adj:
        if node == office:
            path[node] = [office]
        else:
            p = find_path(map, office, node)
            path[node] = p
    return path
  

def FindPath(edges, source, destination):
    status = {}
    adj = build_adjlist(edges)
    for link in edges:
        status[link[0]] = "unvisited"
        status[link[1]] = "unvisited"
    s = Stack()
    s.push([source])
    status[source] = "visiting"
    while not s.isEmpty():
        vertex = s.pop()
        status[vertex[-1]] = "visiting"
        if vertex[-1] == destination:
            return vertex
        for n in adj[vertex[-1]]:
            if status[n] == "unvisited":
                s.push(vertex + [n])
        status[vertex[-1]] = "visited"
                
"""
DFS
"""
def dfs(map, office):    
    path = {}                
    adj = build_adjlist(map)
    for node in adj:
        if node == office:
            path[office] = [office]
        else:
            p = FindPath(map, office, node)
            path[node] = p
    return path
    

"""
Dijkstra's
"""

def dj_adjlist(map):
    adj = {}
    for v in map:
        start = v[0]
        destination = v[1]
        weight = v[2]
        if start not in adj:
            adj[start] = []
        adj[start].append([weight, destination])
    for v in map:
        start = v[1]
        destination = v[0]
        weight = v[2]
        if start not in adj:
            adj[start] = []
        adj[start].append([weight, destination])
    return adj


def initSingleSource(G, source): 
    shortest_distance = {}
    shortest_distance[source] = source
    for vertex in dj_adjlist(G).keys():
        if vertex not in shortest_distance:
            shortest_distance[vertex] = float('inf') 
    shortest_distance[source] = 0
    return shortest_distance


def shortest_path(source, dest, predecessor):
    node = dest
    path = [dest]
    while node != source:
        node = predecessor[node]
       # print("predecessor is", node)
        path.append(node)
        print("path is", path)
    return path[::-1]


def dijkstra(map, office):
    path = {}
    predecessor = {}
    distances = initSingleSource(map, office)
    adj = dj_adjlist(map)
    visited = set()
    heap = []
    sort_list = sorted(distances.items(), key=lambda x:x[0])
    for k in sort_list:
        hq.heappush(heap, (k[1],k[0]))
    for i in sort_list:
        path[office] = [office]
        path[i[0]] = []
    visited.add(office)
    while heap:
        node = hq.heappop(heap)
        print("node is", node)
        visited.add(node[1])
        path[node[1]] = shortest_path(office, node[1], predecessor)
        for v in adj[node[1]]:
            path[office] = [office]
            if v[1] not in visited:
                print("v[1] is", v[1])
                weight = v[0]
                if (distances[node[1]] + weight, node[1]) < (distances[v[1]], v[1]):
                    distances[v[1]] = distances[node[1]] + weight
                    print("distances is", distances)
                    predecessor[v[1]] = node[1]
                    print("predecssors are", predecessor)
        heap = [(distances[k[1]], k[1]) for k in heap]
        hq.heapify(heap)
    return path


m = [('UPS', 'Steuben', 22), ('Richmond Hill', 'Steuben', 22), ('Richmond Hill', 'Hambleton', 18), ('Richmond Hill', 'Owl Ranch', 18), ('Holly Ridge', 'Diehlstadt', 3), ('Holly Ridge', 'Jacob City', 0), ('Holly Ridge', 'Steuben', 17), ('Diehlstadt', 'Brecon', 8), ('Diehlstadt', 'Hambleton', 9), ('Diehlstadt', 'Steuben', 11), ('Steuben', 'Hambleton', 13), ('Steuben', 'Brecon', 25), ('Hambleton', 'Jacob City', 1), ('Jacob City', 'Sunfield', 19), ('Jacob City', 'Brecon', 1), ('Sunfield', 'Brecon', 12)]
