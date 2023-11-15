import json
import csv
import heapq
import math
from datetime import datetime, timedelta
import timeit
from collections import deque

# Graph Class
class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}

    def addVertex(self, vertex):
        self.vertices[vertex.id] = vertex

    def addEdge(self, edge):
        if edge.source not in self.edges:
            self.edges[edge.source] = {}
        self.edges[edge.source][edge.destination] = edge
    
    def haversine(self, lat1, lon1, lat2, lon2): # to calculate closestVertex
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
            distance = self.haversine(latitude, longitude, vertex.latitude, vertex.longitude)
            if distance < min_distance:
                min_distance = distance
                closest_vertex = vertex_id
        
        #print('closest vertex', closest_vertex)
        
        return int(closest_vertex) #vertex id of closest vertex
    
    """    
    def getWeight(self, source_id, destination_id, day_type, hour):
        edge = self.edges.get(source_id,{}).get(destination_id)
        if edge:
            speed = edge.speeds[day_type][hour]
            print(f"Edge from {source_id} to {destination_id}, Speed: {speed}, Length: {edge.length}")
            if speed > 0:
                return edge.length / speed
        print(f"No valid edge or zero speed from {source_id} to {destination_id}")
        return float('infinity')
    """

    """
    def dijkstra(self, start_vertex_id, end_vertex_id, day_type, hour):
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[start_vertex_id] = 0
        pq = [(0, start_vertex_id)]
        visited = set()

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)            
            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            if current_vertex == end_vertex_id:
                return distances[end_vertex_id]
                        
            for neighbor in self.edges.get(current_vertex, {}):
                if neighbor not in visited:
                    weight = self.getWeight(current_vertex, neighbor, day_type, hour)
                    new_distance = current_distance + weight
                    
                    #print(f"New Distance to {neighbor}: {new_distance}")

                    if new_distance < distances[neighbor]:
                        #print(f"Updating {neighbor} in PQ")
                        
                        distances[neighbor] = new_distance
                        heapq.heappush(pq, (new_distance, neighbor))

        print(f"End vertex not reached: {end_vertex_id}, returning infinity")
        return float('infinity')
    """

    def dijkstra(self, start_vertex_id, end_vertex_id, day_type, hour):
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[start_vertex_id] = 0
        pq = [(0, start_vertex_id)]
        visited = set()
        
        iteration_counter = 0
        while pq and iteration_counter < 100:
            current_distance, current_vertex = heapq.heappop(pq)

            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            if current_vertex == end_vertex_id:
                return distances[end_vertex_id]

            for neighbor in self.edges.get(current_vertex, {}):
                if neighbor in visited:
                    continue
                
                edge = self.edges[current_vertex][neighbor]
                
                speed = edge.speeds[day_type][hour]
                weight = edge.length / speed
                
                new_distance = current_distance + weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))
            
            iteration_counter += 1
            
        return float('infinity')