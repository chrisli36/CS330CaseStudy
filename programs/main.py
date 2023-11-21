import timeit
from Simulator import Simulator
from Preprocessing import Preprocessing

def main():

    preprocessor = Preprocessing()

    vertices = preprocessor.processNodes('fulldataset/node_data.json')
    edges = preprocessor.processEdges('fulldataset/edges.csv')
    
    drivers = preprocessor.processDrivers('fulldataset/drivers.csv')
    passengers = preprocessor.processPassengers('fulldataset/passengers.csv')

    start = timeit.default_timer()
    print("\n" + "\\" * 30 + "\nSTARTING SIMULATION\n" + "\\" * 30)

    sim = Simulator()
    sim.setProblem("T1")
    sim.runSimulation(vertices, edges, drivers, passengers)

    print("Time taken: ", timeit.default_timer() - start)

if __name__ == "__main__":
    main()