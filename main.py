import json
import csv
import heapq
import math
from datetime import datetime, timedelta
import timeit
from collections import deque
from T1 import T1
from Preprocessing import Preprocessing
from Graph import Graph

def main():

    preprocessor = Preprocessing()

    vertices = preprocessor.processNodes('node_data.json')
    edges = preprocessor.processEdges('edges.csv')
    #vertices = processNodes('testdataset/test_node.json')
    #edges = processEdges('testdataset/test_edges.csv')
    
    drivers = preprocessor.processDrivers('drivers.csv')
    passengers = preprocessor.processPassengers('passengers.csv')
    #drivers = processDrivers('testdataset/test_drivers.csv')
    #passengers = processPassengers('testdataset/test_passengers.csv')

    graph = Graph()
    for vertex in vertices:
        graph.addVertex(vertex)
    for edge in edges:
        graph.addEdge(edge) 
        
        
    # Usage:
    # Assuming you have an instance of Graph named 'graph'
    start_vertex_id = 1  # Replace with your actual start vertex ID
    end_vertex_id = 100  # Replace with your actual end vertex ID
    
    start = timeit.default_timer()
    print("The start time is:", start)
    algorithm = T1()
    algorithm.baseline_algorithm(graph, drivers, passengers)
    print("The difference ", 
          timeit.default_timer() - start)

if __name__ == "__main__":
    main()