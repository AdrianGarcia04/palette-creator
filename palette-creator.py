import numpy as np
import cv2 as cv
import sys
from random import randint
import centroid

def main():
    # Reading image
    img = cv.imread(sys.argv[1])

    # Dummy image for reference
    dummy = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    # Number of centroids
    k = int(sys.argv[2])
    print('k-centroids: %d' % (k))

    # Image rows, cols and channels
    print('(rows, cols, channels): ' + str(img.shape))

    # Get random centroids
    centroids = randomCentroids(img, k)

    i = 1
    for centroid in centroids:
        print('C' + str(i))
        # Centroid coordinates
        print('(%d, %d)' % (centroid.x, centroid.y))
        # and its respective colors
        print(img[centroid.x, centroid.y])
        print('\n')
        i += 1

    assocPointsToCentroids(img, dummy, centroids)

    # Displaying image
    cv.imshow('image', dummy)
    print('Press any key to exit...')
    cv.waitKey(0)
    cv.destroyAllWindows()

def randomCentroids(img, k):
    imgRows = img.shape[0]
    imgCols = img.shape[1]

    centroids = []

    for _ in range(0, k):
        x = randint(0, imgRows)
        y = randint(0, imgCols)
        rgb = img[x, y]
        centroids.append(centroid.Centroid(x, y, rgb))

    return centroids

def assocPointsToCentroids(img, dummy, centroids):
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            # RGB values in (x, y)
            red = img[x, y][0]
            green = img[x, y][1]
            blue = img[x, y][2]

            distances = []
            for centroid in centroids:
                # The distance between two points
                # is the sum of the squares of the differences
                # between RGB values
                redDiff = int(centroid.red) - int(red)
                greenDiff = int(centroid.green) - int(green)
                blueDiff = int(centroid.blue) - int(blue)
                dist = (redDiff)**2 + (greenDiff)**2 + (blueDiff)**2
                distances.append(dist)

            # Corresponding centroid
            minDistCluster = distances.index(min(distances))
            centroid = centroids[minDistCluster]

            centroid.assoc((x, y))

            dummy[x, y] = (centroid.red, centroid.green, centroid.blue)


main()
