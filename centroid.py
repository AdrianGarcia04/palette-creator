class Centroid:

    def __init__(self, x, y, rgb):
        self.prev = None
        self.x = x
        self.y = y
        self.rgb = rgb
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]

    def __str__(self):
        return '[%2d, %2d] : (%2d, %2d, %2d)' % (self.x, self.y, self.red, self.green, self.blue)

    def alikePrev(self, diff):
        if self.prev == None:
            return False
        redDiff = abs(self.red - self.prev.red)
        greenDiff = abs(self.green - self.prev.green)
        blueDiff = abs(self.blue - self.prev.blue)
        return redDiff < diff and greenDiff < diff and blueDiff < diff
