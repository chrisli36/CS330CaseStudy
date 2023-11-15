import json
import csv
import heapq
import math
from datetime import datetime, timedelta
import timeit

# Vertex Classe
class Vertex:
    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        
# Edge Class
class Edge:
    def __init__(self, source, destination, length, speeds):
        self.source = source
        self.destination = destination
        self.length = length
        self.speeds = speeds  # Dictionary containing speeds for different hours and day types

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
        
        print('closest vertex', closest_vertex)
        
        return int(closest_vertex) #vertex id of closest vertex
    
    def getWeight(self, source_id, destination_id, day_type, hour):
        edge = self.edges.get(source_id,{}).get(destination_id)
        if edge:
            speed = edge.speeds[day_type][hour]
            print(f"Edge from {source_id} to {destination_id}, Speed: {speed}, Length: {edge.length}")
            if speed > 0:
                return edge.length / speed
        print(f"No valid edge or zero speed from {source_id} to {destination_id}")
        return float('infinity')

    def dijkstra(self, start_vertex_id, end_vertex_id, day_type, hour):
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[start_vertex_id] = 0
        pq = [(0, start_vertex_id)]
        visited = set()

        while pq:
            #initialize
            current_distance, current_vertex = heapq.heappop(pq)
            visited.add(current_vertex)
            #print(f"Current Vertex: {current_vertex}, Distance: {current_distance}")
            
            # return distance if currenct vertex is destination
            if current_vertex == end_vertex_id:
                print(f"End vertex reached: {end_vertex_id}, Distance: {distances[end_vertex_id]}")
                return distances[end_vertex_id]

            # else skip vertex if it is visited
            if current_vertex in visited:
                continue
            
            # else check and update distance 
            for neighbor in self.edges.get(current_vertex, {}):
                edge = self.edges[current_vertex][neighbor]
                weight = self.getWeight(current_vertex, neighbor, day_type, hour)
                #print(f"Neighbor: {neighbor}, Weight: {weight}")
                new_distance = current_distance + weight
                #print(f"New Distance to {neighbor}: {new_distance}")

                if new_distance < distances[neighbor]:
                    #print(f"Updating {neighbor} in PQ")
                    distances[neighbor] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))

        print(f"End vertex not reached: {end_vertex_id}, returning infinity")
        return distances.get(end_vertex_id, float('infinity'))

# Preprocessing
def processNodes(fileName):
    with open(fileName, 'r') as file:
        node_data = json.load(file)
    vertices = []
    for node_id, coords in node_data.items():
        vertex = Vertex(int(node_id), float(coords['lat']), float(coords['lon']))
        vertices.append(vertex)
    return vertices

def processEdges(fileName):
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


def processDrivers(fileName):
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

def processPassengers(fileName):
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

# T1
def baseline_algorithm(graph, drivers, passengers):
    # give id to driver to distinguish driver
    for i, driver in enumerate(drivers):
        driver['id'] = i

    # track 
    total_passenger_wait_time = 0
    total_driver_active_time = 0
    driver_active_times = {driver['id']: 0 for driver in drivers}
    
    for passenger in passengers:
        p_vertex = graph.closestVertex(passenger['source_lat'], passenger['source_lon'])
        dropoff_vertex = graph.closestVertex(passenger['dest_lat'], passenger['dest_lon'])

        nearest_driver = None
        min_distance = float('infinity')
        min_time_to_pickup = None
         

        for driver in drivers:
            d_vertex = graph.closestVertex(driver['latitude'], driver['longitude'])
            day_type = 'weekday' if (driver['datetime']).weekday() < 5 else 'weekend'
            hour = driver['datetime'].hour

            time_to_pickup = graph.dijkstra(d_vertex, p_vertex, day_type, hour)
            time_to_dropoff = graph.dijkstra(p_vertex, dropoff_vertex, day_type, hour)
            
            #print(time_to_dropoff)
            #print(time_to_pickup)

            if time_to_pickup < min_distance:
                min_distance = time_to_pickup
                min_time_to_pickup = time_to_pickup
                nearest_driver = driver

        if nearest_driver:
            passenger_wait_time = (passenger['datetime'] -nearest_driver['datetime']).total_seconds()
            total_passenger_wait_time += passenger_wait_time

            trip_time = min_time_to_pickup + time_to_dropoff
            total_driver_active_time += trip_time
            
            # update active time with driver id
            driver_active_times[nearest_driver['id']] += trip_time

            # update driver location and time
            nearest_driver['latitude'], nearest_driver['longitude'] = passenger['dest_lat'], passenger['dest_lon']
            nearest_driver['datetime'] = nearest_driver['datetime'] + timedelta(seconds=time_to_dropoff)

            # Check if driver's active time exceeds 8 hours
            if driver_active_times[nearest_driver['id']] >= 28800:
                drivers.remove(nearest_driver)

    total_passenger_wait_time /= 60  # Convert to minutes
    total_driver_active_time /= 60   # Convert to minutes

    #print("Total Passenger Wait Time (D1):", total_passenger_wait_time, "minutes")
    #print("Total Driver Active Time (D2):", total_driver_active_time, "minutes")



def main():
    vertices = processNodes('node_data.json')
    edges = processEdges('edges.csv')
    #vertices = processNodes('testdataset/test_node.json')
    #edges = processEdges('testdataset/test_edges.csv')
    
    drivers = processDrivers('drivers.csv')
    passengers = processPassengers('passengers.csv')
    #drivers = processDrivers('testdataset/test_drivers.csv')
    #passengers = processPassengers('testdataset/test_passengers.csv')

    graph = Graph()
    for vertex in vertices:
        graph.addVertex(vertex)
    for edge in edges:
        graph.addEdge(edge)
        
        
    start = timeit.default_timer()
    print("The start time is:", start)
    baseline_algorithm(graph, drivers, passengers)
    print("The difference ", 
          timeit.default_timer() - start)

if __name__ == "__main__":
    main()