# Edge Class
class Edge:
    def __init__(self, source, dest, length, speeds):
        self.source = source
        self.dest = dest
        self.length = length
        self.speeds = speeds  # Dictionary containing speeds for different hours and day types
