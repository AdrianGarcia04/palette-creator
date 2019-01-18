class Centroid:

    def __init__(self, x, y, rgb):
        self.x = x
        self.y = y
        self.rgb = rgb
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]

    def __str__(self):
        return '[%2d, %2d] : (%2d, %2d, %2d)' % (self.x, self.y, self.red, self.green, self.blue)
