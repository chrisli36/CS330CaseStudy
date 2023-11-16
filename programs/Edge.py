# Edge Class
class Edge:
    def __init__(self, source, destination, length, speeds):
        self.source = source
        self.destination = destination
        self.length = length
        self.speeds = speeds  # Dictionary containing speeds for different hours and day types
