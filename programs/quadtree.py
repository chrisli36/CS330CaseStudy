from datetime import datetime
from Vertex import Vertex
from Edge import Edge
from Graph import Graph


#boundary (x, y, width, height)
# x = mean(min(vertex.lon), max(vertex.lon))
# y = mean(min(vertex.lat), max(vertex.lon))
# width = max(vertex.lon) - min(vertex.lon)
# height = max(vertex.lat) - min(vertex.lat)


class QuadTreeNode:
    def __init__(self, lat, lon, id):
        self.lat = lat
        self.lon = lon
        self.id = id

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        min_lat, min_lon, max_lat, max_lon = self.boundary
        mid_lat = (min_lat + max_lat) / 2
        mid_lon = (min_lon + max_lon) / 2

        self.northwest = QuadTree((min_lat, min_lon, mid_lat, mid_lon), self.capacity)
        self.northeast = QuadTree((min_lat, mid_lon, mid_lat, max_lon), self.capacity)
        self.southwest = QuadTree((mid_lat, min_lon, max_lat, mid_lon), self.capacity)
        self.southeast = QuadTree((mid_lat, mid_lon, max_lat, max_lon), self.capacity)

        self.divided = True

    def insert(self, vertex):
        if not self.in_boundary(vertex.lat, vertex.lon):
            return False

        if len(self.points) < self.capacity:
            self.points.append(vertex)
            return True
        else:
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

        return False

    def in_boundary(self, lat, lon):
        min_lat, min_lon, max_lat, max_lon = self.boundary
        return min_lon <= lon < max_lon and min_lat <= lat < max_lat

    def query_range(self, range, found=None):
        if found is None:
            found = []

        if not self.intersects_range(range):
            return found

        for point in self.points:
            if self.point_in_range(point, range):
                found.append(point)

        if self.divided:
            self.nw.query_range(range, found)
            self.ne.query_range(range, found)
            self.sw.query_range(range, found)
            self.se.query_range(range, found)

        return found

    def intersects_range(self, range):
        x, y, w, h = self.boundary
        rx, ry, rw, rh = range

        return not (x + w < rx or x > rx + rw or y + h < ry or y > ry + rh)

    def point_in_range(self, point, range):
        x, y, w, h = range
        return x <= point.x < x + w and y <= point.y < y + h
    
    def find_closest(self, lat, lon, search_radius = 0.01, increment=0.01):
        # find closest vertex to the given latitude and longitutde
        while True:
            range_to_query = (lat - search_radius, lon - search_radius, search_radius *2, search_radius*2)
            found_points = self.query_range(range_to_query)
            
            if found_points:
                return min(found_points, key=lambda p: Graph.getDistance(p.lat, p.lon, lat, lon))
            search_radius += increment
