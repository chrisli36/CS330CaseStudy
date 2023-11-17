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
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary
        nw = QuadTree((x, y, w/2, h/2), self.capacity)
        ne = QuadTree((x + w/2, y, w/2, h/2), self.capacity)
        sw = QuadTree((x, y + h/2, w/2, h/2), self.capacity)
        se = QuadTree((x + w/2, y + h/2, w/2, h/2), self.capacity)
        self.nw = nw
        self.ne = ne
        self.sw = sw
        self.se = se
        self.divided = True

    def insert(self, point):
        if not self.in_boundary(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.nw.insert(point) or self.ne.insert(point) or self.sw.insert(point) or self.se.insert(point):
                return True

        return False

    def in_boundary(self, point):
        x, y, w, h = self.boundary
        return x <= point.x < x + w and y <= point.y < y + h

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
            found_points = self.query_range(range(range_to_query))
            
            if found_points:
                return min(found_points, key=lambda p: Graph.getDistance(p.lat, p.lon, lat, lon))
            search_radius += increment
