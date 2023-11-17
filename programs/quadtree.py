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
        if not self.in_boundary(vertex.lat, vertex.lon):
            return False

        if len(self.vertices) < self.capacity:
            self.vertices.append(vertex)
            return True
        
        if not self.divided:
            self.subdivide()
            
        if self.northwest.insert(vertex):
            return True
        elif self.northeast.insert(vertex):
            return True
        elif self.southwest.insert(vertex):
            return True
        elif self.southeast.insert(vertex):
            return True
        
        print("INSERT FAILED")
        return False

    def in_boundary(self, lat, lon):
        min_lat, min_lon, max_lat, max_lon = self.boundary
        return min_lon <= lon <= max_lon and min_lat <= lat <= max_lat

    def subdivide(self):
        min_lat, min_lon, max_lat, max_lon = self.boundary
        mid_lat = (min_lat + max_lat) / 2
        mid_lon = (min_lon + max_lon) / 2

        self.northwest = QuadTree((min_lat, min_lon, mid_lat, mid_lon), self.capacity)
        self.northeast = QuadTree((min_lat, mid_lon, mid_lat, max_lon), self.capacity)
        self.southwest = QuadTree((mid_lat, min_lon, max_lat, mid_lon), self.capacity)
        self.southeast = QuadTree((mid_lat, mid_lon, max_lat, max_lon), self.capacity)

        self.divided = True

        for vertex in self.vertices:
            if self.northwest.insert(vertex):
                continue
            elif self.northeast.insert(vertex):
                continue
            elif self.southwest.insert(vertex):
                continue
            elif self.southeast.insert(vertex):
                continue
            print("SOMETHING'S WRONG")

    def getDistance(self, lat1, lon1, lat2, lon2): # to calculate closestVertex
        R = 3959.87433   
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    def find_closest(self, lat, lon):
        if self.divided:
            if self.northwest.in_boundary(lat, lon) and len(self.northwest.vertices) > 0:
                return self.northwest.find_closest(lat, lon)
            elif self.northeast.in_boundary(lat, lon) and len(self.northeast.vertices) > 0:
                return self.northeast.find_closest(lat, lon)
            elif self.southwest.in_boundary(lat, lon) and len(self.southwest.vertices) > 0:
                return self.southwest.find_closest(lat, lon)
            elif self.southeast.in_boundary(lat, lon) and len(self.southeast.vertices) > 0:
                return self.southeast.find_closest(lat, lon)
        
        # fix this later it needs to iterate through children
        min_distance = float("inf"); closest_vertex = None
        for vertex in self.vertices:
            distance = self.getDistance(lat, lon, vertex.lat, vertex.lon)
            # print(distance)
            if distance < min_distance:
                min_distance = distance
                closest_vertex = vertex.id
        return int(closest_vertex) #vertex id of closest vertex