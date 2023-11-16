import timeit
from T1 import T1
from Preprocessing import Preprocessing
from Graph import Graph

def main():

    preprocessor = Preprocessing()

    vertices = preprocessor.processNodes('node_data.json')
    edges = preprocessor.processEdges('edges.csv')
    
    drivers = preprocessor.processDrivers('drivers.csv')
    passengers = preprocessor.processPassengers('passengers.csv')

    graph = Graph()
    for vertex in vertices:
        graph.addVertex(vertex)
    for edge in edges:
        graph.addEdge(edge) 
    
    start = timeit.default_timer()
    print("The start time is:", start)
    algorithm = T1()
    algorithm.baseline_algorithm(graph, drivers, passengers)
    print("The difference ", 
          timeit.default_timer() - start)

if __name__ == "__main__":
    main()