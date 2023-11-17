import math

# given point, traverse tree, return 1-4 point that fall within the rectangle of the tree
# return point min distance

class QuadTreeNode:
    def __init__(self, lat, lon, id):
        self.lat = lat
        self.lon = lon
        self.id = id

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary #  boundary = (min_lat, min_lon, max_lat, max_lon)
        self.capacity = capacity
        self.vertices = []
        self.divided = False
        
    def insert(self, vertex):
        if not self.inBoundary(vertex.lat, vertex.lon):
            return False

        if len(self.vertices) < self.capacity:
            self.vertices.append(vertex)
            return True
        
        if not self.divided:
            self.subdivide()
            
        for quad in self.quads:
            if quad.insert(vertex):
                return True

        print("INSERT FAILED")
        return False

    def inBoundary(self, lat, lon):
        min_lat, min_lon, max_lat, max_lon = self.boundary
        return min_lon <= lon <= max_lon and min_lat <= lat <= max_lat

    def subdivide(self):
        min_lat, min_lon, max_lat, max_lon = self.boundary
        mid_lat = (min_lat + max_lat) / 2
        mid_lon = (min_lon + max_lon) / 2

        northwest = QuadTree((min_lat, min_lon, mid_lat, mid_lon), self.capacity)
        northeast = QuadTree((min_lat, mid_lon, mid_lat, max_lon), self.capacity)
        southwest = QuadTree((mid_lat, min_lon, max_lat, mid_lon), self.capacity)
        southeast = QuadTree((mid_lat, mid_lon, max_lat, max_lon), self.capacity)
        self.quads = [northwest, northeast, southwest, southeast]

        self.divided = True

        for vertex in self.vertices:
            quadID = self.getQuadID(vertex.lat, vertex.lon, self.quads)
            self.quads[quadID].insert(vertex)

    def getQuadID(self, lat, lon, quads):
        for i, quad in enumerate(quads):
            # print(quad.boundary)
            if quad.inBoundary(lat, lon):
                return i
        print("Did not find a quad for {}, {}".format(lat, lon))
        return None

    def getDistance(self, lat1, lon1, lat2, lon2):
        R = 3959.87433   
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    def findClosest(self, lat, lon):
        if self.divided:
            quadID = self.getQuadID(lat, lon, self.quads)
            quad = self.quads[quadID]
            if quad.inBoundary(lat, lon) and len(quad.vertices) > 0:
                return quad.findClosest(lat, lon)
            return self.chooseClosest(lat, lon, self.getAllChildren())
        return self.chooseClosest(lat, lon, self.vertices)
        
    def chooseClosest(self, lat, lon, vertices):
        min_distance = float("inf"); closest_vertex = None
        for vertex in vertices:
            distance = self.getDistance(lat, lon, vertex.lat, vertex.lon)
            # print(distance)
            if distance < min_distance:
                min_distance = distance
                closest_vertex = vertex.id
        return int(closest_vertex) #vertex id of closest vertex
                
    def getAllChildren(self):
        children = []
        for quad in self.quads:
            children.extend(quad.vertices)
        return children