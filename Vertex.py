import json
import csv
import heapq
import math
from datetime import datetime, timedelta
import timeit
from collections import deque

# Vertex Classe
class Vertex:
    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude