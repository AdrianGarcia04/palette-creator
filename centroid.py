class Centroid:

    def __init__(self, x, y, rgb):
        self.x = x
        self.y = y
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]
        self.points = []

    def assoc(self, point):
        self.points.append(point)
