import json
import csv
from datetime import datetime
from Vertex import Vertex
from Edge import Edge
from Driver import Driver

class Preprocessing:
    def processNodes(self, fileName):
        '''Returns a list of vertex objects'''

        with open(fileName, 'r') as file:
            node_data = json.load(file)
        vertices = []
        for node_id, coords in node_data.items():
            vertex = Vertex(int(node_id), float(coords['lat']), float(coords['lon']))
            vertices.append(vertex)
        
        print("Processed nodes!")
        return vertices

    def processEdges(self, fileName):
        '''Returns a list of edge objects'''

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
                edges.append(edge)
        
        print("Processed edges!")
        return edges


    def processDrivers(self, fileName):
        '''Returns a list of drivers where each driver is a dictionary {datetime, latitutde, longitude}'''

        drivers = []
        with open(fileName, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                
                driver = Driver()

                drivers.append({
                    'datetime': datetime.strptime(row['Date/Time'], "%m/%d/%Y %H:%M:%S"),
                    'latitude': float(row['Source Lat']),
                    'longitude': float(row['Source Lon'])
                })

        print("Processed drivers!")
        return drivers

    def processPassengers(self, fileName):
        '''Returns a list of passengers where each passenger is a dictionary {datetime, source_lat, source_lon, dest_lat, dest_lon}'''

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

        print("Processed passengers!")
        return passengers