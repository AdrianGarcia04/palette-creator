class Cluster:

    def __init__(self, centroid):
        self.centroid = centroid
        self.points = {}

    def addPoint(self, x, y, rgb):
        self.points[(x, y)] = rgb
