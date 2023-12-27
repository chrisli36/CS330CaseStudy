import json
import csv
from datetime import datetime
from Vertex import Vertex
from Edge import Edge
from Driver import Driver
from Passenger import Passenger

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
        '''Returns a list of driver objects'''

        drivers = []
        with open(fileName, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                dt = datetime.strptime(row['Date/Time'], "%m/%d/%Y %H:%M:%S")
                lat = float(row['Source Lat']); lon = float(row['Source Lon'])
                driver = Driver(dt, lat, lon)
                drivers.append(driver)

        print("Processed drivers!")
        return drivers

    def processPassengers(self, fileName):
        '''Returns a list of passenger objects'''

        passengers = []
        with open(fileName, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                dt = datetime.strptime(row['Date/Time'], "%m/%d/%Y %H:%M:%S")
                slat = float(row['Source Lat']); slon = float(row['Source Lon'])
                dlat = float(row['Dest Lat']); dlon = float(row['Dest Lon'])
                passenger = Passenger(dt, slat, slon, dlat, dlon)
                passengers.append(passenger)

        print("Processed passengers!")
        return passengers