import sys

class Cluster:

    def __init__(self, centroid):
        self.prev = None
        self.centroid = centroid
        self.points = []
        self.minDist = sys.maxint

    def addPoint(self, point):
        self.points.append(point)
