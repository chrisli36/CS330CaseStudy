import json
import csv
import heapq
import math
from datetime import datetime, timedelta
import timeit
from collections import deque
from T1 import T1
from Vertex import Vertex
from Edge import Edge
from Graph import Graph

class Preprocessing:
    # Preprocessing
    def processNodes(self, fileName):
        with open(fileName, 'r') as file:
            node_data = json.load(file)
        vertices = []
        for node_id, coords in node_data.items():
            vertex = Vertex(int(node_id), float(coords['lat']), float(coords['lon']))
            vertices.append(vertex)
        return vertices

    def processEdges(self, fileName):
        edges = []
        with open(fileName, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                source, dest, length = int(row[0]), int(row[1]), float(row[2])
                speeds = {
                    'weekday': {hour: float(row[3 + hour]) for hour in range(24)},
                    'weekend': {hour: float(row[27 + hour]) for hour in range(24)}
                }
                edge = Edge(source, dest, length, speeds)
                
                #This seems fine
                #print(f"Edge from {source} to {dest}, length: {length}, speeds: {speeds}")
                
                edges.append(edge)
        return edges


    def processDrivers(self, fileName):
        drivers = []
        with open(fileName, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                drivers.append({
                    'datetime': datetime.strptime(row['Date/Time'], "%m/%d/%Y %H:%M:%S"),
                    'latitude': float(row['Source Lat']),
                    'longitude': float(row['Source Lon'])
                })
        #print(drivers[-1])
        return drivers

    def processPassengers(self, fileName):
        passengers = []
        with open(fileName, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                passengers.append({
                    'datetime': datetime.strptime(row['Date/Time'], "%m/%d/%Y %H:%M:%S"),
                    'source_lat': float(row['Source Lat']),
                    'source_lon': float(row['Source Lon']),
                    'dest_lat': float(row['Dest Lat']),
                    'dest_lon': float(row['Dest Lon'])
                })
        #print(passengers)
        return passengers