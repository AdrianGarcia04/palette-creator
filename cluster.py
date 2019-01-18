class Cluster:

    def __init__(self, centroid):
        self.centroid = centroid
        self.points = []

    def addPoint(self, point):
        self.points.append(point)
