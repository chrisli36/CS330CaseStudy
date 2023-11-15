import json

#attempt to use adjacency-1 doesnt work

# Vertex Class
class Vertex:
    def __init__(self, node_id, latitude, longitude):
        self.id = node_id
        self.latitude = latitude
        self.longitude = longitude

# Edge Class
class Edge:
    def __init__(self, start, end, attributes):
        self.start = start
        self.end = end
        self.attributes = attributes

# Graph Class
class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}

    def addVertex(self, vertex):
        self.vertices[vertex.id] = vertex

    def addEdge(self, edge):
        if edge.start not in self.edges:
            self.edges[edge.start] = {}
        self.edges[edge.start][edge.end] = edge.attributes

# Preprocessing Functions
def processNodes(fileName):
    with open(fileName, 'r') as file:
        node_data = json.load(file)

    graph = Graph()
    for node_id, coords in node_data.items():
        vertex = Vertex(int(node_id), float(coords['lat']), float(coords['lon']))
        graph.addVertex(vertex)
    return graph

def processEdges(fileName, graph):
    with open(fileName, 'r') as file:
        adjacency_data = json.load(file)

    for start_node, connections in adjacency_data.items():
        for end_node, attributes in connections.items():
            edge = Edge(int(start_node), int(end_node), attributes)
            graph.addEdge(edge)

# Main Function
def main():
    graph = processNodes('node_data.json')
    processEdges('adjacency-1.json', graph)
    
    print(graph)
    print(processEdges('adjacency.json', graph))


    # The graph is now populated with vertices and edges
    # You can add additional functionality as required

if __name__ == "__main__":
    main()





"""
def verify_graph_construction(vertices, edges):
    graph = Graph()

    # Add vertices to the graph
    for vertex in vertices:
        graph.addVertex(vertex)

    # Add edges to the graph
    for edge in edges:
        graph.addEdge(edge)

    # Check if all vertices are in the graph
    for vertex in vertices:
        if vertex.id not in graph.vertices:
            print(f"Vertex {vertex.id} is missing in the graph.")
            return False

    # Check if all edges are in the graph and have correct weights
    for edge in edges:
        if edge.source not in graph.edges or edge.destination not in graph.edges[edge.source]:
            print(f"Edge from {edge.source} to {edge.destination} is missing in the graph.")
            return False

        # Check if the weight calculation is correct
        weight = graph.getWeight(edge.source, edge.destination, 'weekend', 22) 
        if weight == float('infinity') or weight <= 0:
            print(f"Edge from {edge.source} to {edge.destination} has invalid weight: {weight}")
            return False

    print("Graph construction is correct.")
    return True
"""