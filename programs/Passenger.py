class Passenger:
    def __init__(self, datetime, source_lat, source_lon, dest_lat, dest_lon):
        self.datetime = datetime
        self.source_lat = source_lat
        self.source_lon = source_lon
        self.dest_lat = dest_lat
        self.dest_lon = dest_lon
        self.timeActive = 0