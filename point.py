class Point:

    def __init__(self, x, y, rgb):
        self.x = x
        self.y = y
        self.rgb = rgb
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]
        self.distSum = 0
