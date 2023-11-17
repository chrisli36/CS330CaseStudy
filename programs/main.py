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

    start = timeit.default_timer()
    print("\n" + "\\" * 30 + "\nSTARTING SIMULATION\n" + "\\" * 30)

    algorithm = T1()
    algorithm.runT1(vertices, edges, drivers, passengers)
    print("Time taken: ", timeit.default_timer() - start)

if __name__ == "__main__":
    main()