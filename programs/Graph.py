import heapq
import math
from collections import defaultdict
from Quadtree import QuadTree, QuadTreeNode

# Graph Class
class Graph:
    def __init__(self, vertices, edges):
        self.vertices = []
        self.oldToNew = {}
        for vertex in vertices:
            self.addVertex(vertex)
        self.V = len(self.vertices)

        self.edges = defaultdict(dict)
        # self.adjacency = defaultdict(dict)
        for edge in edges:
            self.addEdge(edge)

        self.initQuadTree(vertices)

    def addVertex(self, vertex):
        newID = len(self.vertices)

        self.oldToNew[vertex.id] = newID
        vertex.id = newID
        self.vertices.append(vertex)

    def addEdge(self, edge):
        edge.source = self.oldToNew[edge.source]
        edge.dest = self.oldToNew[edge.dest]

        self.edges[edge.source][edge.dest] = edge
        # self.adjacency[edge.source][](edge.dest)
        # self.adjacency[edge.dest].append(edge.source)
        
    def initQuadTree(self, vertices):
        # find the boundary
        allLatitudes = [vertex.lat for vertex in vertices]
        allLongitudes = [vertex.lon for vertex in vertices]
        boundary = (min(allLatitudes) - 2, min(allLongitudes) - 2, max(allLatitudes) + 2, max(allLongitudes) + 2)
        
        # build tree
        self.qt = QuadTree(boundary, 4)
        for vertex in vertices:
            node = QuadTreeNode(vertex.lat, vertex.lon, vertex.id)
            self.qt.insert(node)
    
    def getDistance(self, lat1, lon1, lat2, lon2): # to calculate closestVertex
        R = 3959.87433   
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    def closestVertex(self, lat, lon):
        minDistance = float("inf"); closestID = None
        for id, vertex in enumerate(self.vertices):
            distance = self.getDistance(lat, lon, vertex.lat, vertex.lon)
            if distance < minDistance:
                minDistance = distance
                closestID = id
        return int(closestID) # vertex id of closest vertex
    
    def closestVertexQT(self, lat, lon):
        return self.qt.findClosest(lat, lon)
       
    def getWeight(self, sourceID, destID, day_type, hour):
        # print(self.edges[sourceID])
        # print(sourceID, destID)
        edge = self.edges[sourceID][destID]
        if edge:
            speed = edge.speeds[day_type][hour]
            if speed > 0:
                return edge.length / speed
        print(f"No valid edge or zero speed from {sourceID} to {destID}")
        return float('inf')

    def dijkstra(self, startID, endID, datetime):
        if startID == endID:
            return 0.0

        day_type = 'weekday' if datetime.weekday() < 5 else 'weekend'
        hour = datetime.hour

        times = [float('inf')] * self.V; times[startID] = 0
        pq = [(0, startID)]
        visited = set()
        while pq:
            currDistance, currVertex = heapq.heappop(pq)
            if currVertex in visited:
                continue
            visited.add(currVertex)
            
            for neighbor, _ in self.edges[currVertex].items():
                if neighbor not in visited:
                    weight = self.getWeight(currVertex, neighbor, day_type, hour)

                    newTime = currDistance + weight
                    if newTime < times[neighbor]:
                        times[neighbor] = newTime
                        heapq.heappush(pq, (newTime, neighbor))

                        if neighbor == endID:
                            return 3600 * times[endID]

        print(f"Could not find path from {startID} to {endID}, returning infinity")
        return float('inf')
    
    def astar(self, startID, endID, datetime):
        if startID == endID:
            return 0.0
        
        day_type = 'weekday' if datetime.weekday() < 5 else 'weekend'
        hour = datetime.hour

        times = [float('inf')] * self.V; times[startID] = 0
        pq = [(0, startID)]
        visited = set()
        tlat = self.vertices[endID].lat; tlon = self.vertices[endID].lon
        while pq:
            _, currVertex = heapq.heappop(pq)            
            if currVertex in visited:
                continue
            visited.add(currVertex)
                        
            for neighbor, _ in self.edges[currVertex].items():
                if neighbor not in visited:
                    weight = self.getWeight(currVertex, neighbor, day_type, hour)

                    slat = self.vertices[neighbor].lat; slon = self.vertices[neighbor].lon
                    distHeuristic = 0.04 * self.getDistance(slat, slon, tlat, tlon)

                    newTime = times[currVertex] + weight
                    heuristicDistance = newTime + distHeuristic

                    # print(distHeuristic, newTime)

                    if newTime < times[neighbor]:
                        times[neighbor] = newTime
                        heapq.heappush(pq, (heuristicDistance, neighbor))

                        if neighbor == endID:
                            return 3600 * times[endID]

        print(f"Could not find path from {startID} to {endID}, returning infinity")
        return float('inf')
    
    def getAverageWeight(self, edge):
        times = []
        for dayType in ['weekday', 'weekend']:
            for hour in range(24):
                time = edge.speeds[dayType][hour]
                times.append(time)
        return sum(times) / len(times)

    def runFloydWarshall(self):
        print("Running Floyd-Warshall preprocessing!")
        graph = []
        for i in range(self.V):
            print("\titeration {}".format(i))
            graph.append([float("inf")] * self.V)
        print("Finished initializing infinities")
        for u, vs in self.edges.items():
            for v, edge in vs.items():
                graph[u][v] = self.getAverageWeight(edge)
        print("Finished initializing graph")

        times = list(map(lambda i: list(map(lambda j: j, i)), graph))
        for k in range(self.V):
            print("\titeration {}".format(k))
            for i in range(self.V):
                for j in range(self.V):
                    times[i][j] = min(times[i][j], times[i][k] + times[k][j])
        self.estimatedTimes = times
    
    def floydWarshall(self, startID, endID):
        return self.estimatedTimes[startID][endID]