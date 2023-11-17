import heapq
import math
from collections import defaultdict
from Quadtree import QuadTree, QuadTreeNode

# Graph Class
class Graph:
    def __init__(self, vertices, edges):
        self.vertices = {}
        for vertex in vertices:
            self.addVertex(vertex)
        self.edges = {}
        for edge in edges:
            self.addEdge(edge)

        self.adjacency = defaultdict(list)
        self.initQuadTree(vertices)
        
    def initQuadTree(self, vertices):
        # find the boundary
        allLatitudes = [vertex.latitude for vertex in vertices]
        allLongitudes = [vertex.longitude for vertex in vertices]
        boundary = (min(allLatitudes), min(allLongitudes), max(allLatitudes), max(allLongitudes))
        
        # build tree
        self.qt = QuadTree(boundary, 4)
        for vertex in vertices:
            node = QuadTreeNode(vertex.latitude, vertex.longitude, vertex.id)
            self.qt.insert(node)

    def addVertex(self, vertex):
        self.vertices[vertex.id] = vertex

    def addEdge(self, edge):
        if edge.source not in self.edges:
            self.edges[edge.source] = {}
        self.edges[edge.source][edge.destination] = edge

        self.adjacency[edge.source].append(edge.destination)
        self.adjacency[edge.destination].append(edge.source)
    
    def getDistance(self, lat1, lon1, lat2, lon2): # to calculate closestVertex
        R = 3959.87433   
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    def closestVertex(self, latitude, longitude):
        min_distance = float("inf")
        closest_vertex = None
        for vertex_id, vertex in self.vertices.items():
            distance = self.getDistance(latitude, longitude, vertex.latitude, vertex.longitude)
            if distance < min_distance:
                min_distance = distance
                closest_vertex = vertex_id
        return int(closest_vertex) #vertex id of closest vertex
    
    def closestVertexQT(self, latitude, longitude):
        return self.qt.find_closest(latitude, longitude)
       
    def getWeight(self, source_id, destination_id, day_type, hour):
        edge = self.edges[source_id][destination_id]
        if edge:
            speed = edge.speeds[day_type][hour]
            if speed > 0:
                return edge.length / speed
        print(f"No valid edge or zero speed from {source_id} to {destination_id}")
        return float('inf')


    def dijkstra(self, start_vertex_id, end_vertex_id, day_type, hour):
        if start_vertex_id == end_vertex_id:
            return 0.0

        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex_id] = 0

        pq = [(0, start_vertex_id)]
        visited = set()

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)            
            if current_vertex in visited:
                continue
            visited.add(current_vertex)
                        
            for neighbor in self.adjacency[current_vertex]:
                if neighbor not in visited:
                    weight = self.getWeight(current_vertex, neighbor, day_type, hour)

                    new_distance = current_distance + weight

                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        heapq.heappush(pq, (new_distance, neighbor))

                        if neighbor == end_vertex_id:
                            return 3600 * distances[end_vertex_id]

        print(f"Could not find path from {start_vertex_id} to {end_vertex_id}, returning infinity")
        return float('inf')
    
    def astar(self, start_vertex_id, end_vertex_id, day_type, hour):
        if start_vertex_id == end_vertex_id:
            return 0.0

        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex_id] = 0
        # heuristicDistances = {vertex: float('inf') for vertex in self.vertices}
        # heuristicDistances[start_vertex_id] = 0

        pq = [(0, 0, start_vertex_id)]
        visited = set()

        tlat = self.vertices[end_vertex_id].latitude; tlon = self.vertices[end_vertex_id].longitude

        while pq:
            currHeuristicDistance, current_distance, current_vertex = heapq.heappop(pq)            
            if current_vertex in visited:
                continue
            visited.add(current_vertex)
                        
            for neighbor in self.adjacency[current_vertex]:
                if neighbor not in visited:
                    weight = self.getWeight(current_vertex, neighbor, day_type, hour)

                    slat = self.vertices[neighbor].latitude; slon = self.vertices[neighbor].longitude
                    heuristic = 30 * self.getDistance(slat, slon, tlat, tlon)

                    new_distance = current_distance + weight
                    heuristicDistance = new_distance + heuristic

                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        heapq.heappush(pq, (heuristicDistance, new_distance, neighbor))

                        if neighbor == end_vertex_id:
                            return 3600 * distances[end_vertex_id]

        print(f"Could not find path from {start_vertex_id} to {end_vertex_id}, returning infinity")
        return float('inf')