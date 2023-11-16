import timeit
from T1 import T1
from Preprocessing import Preprocessing
from Graph import Graph

def main():

    preprocessor = Preprocessing()

    vertices = preprocessor.processNodes('fulldataset/node_data.json')
    edges = preprocessor.processEdges('fulldataset/edges.csv')
    
    drivers = preprocessor.processDrivers('fulldataset/drivers.csv')
    passengers = preprocessor.processPassengers('fulldataset/passengers.csv')

    graph = Graph()
    for vertex in vertices:
        graph.addVertex(vertex)
    for edge in edges:
        graph.addEdge(edge) 
    
    start = timeit.default_timer()
    print("The start time is:", start)

    print(drivers[0:10])
    print(passengers[0:10])

    algorithm = T1()
    algorithm.runT1v2(graph, drivers, passengers)
    print("Time taken: ", timeit.default_timer() - start)

if __name__ == "__main__":
    main()