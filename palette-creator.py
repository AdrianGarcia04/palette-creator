import numpy as np
import cv2 as cv
import sys
from random import randint
import centroid
import cluster as clst
import point
from operator import attrgetter

def main():

    # Reading image
    img = cv.imread(sys.argv[1])

    # Dummy image for reference
    dummy = np.zeros((img.shape[0] + 50, img.shape[1] + 20, 3), np.uint8)
    # Make white
    dummy[0:img.shape[0] + 50, 0:img.shape[1] + 20] = (255, 255, 255)

    # Number of centroids
    k = int(sys.argv[2])
    print('k-centroids: %d' % (k))

    # Max difference between RGB values to tell if the found mean is correct
    MAX_DIFF_RGB = int(sys.argv[5]) or 10

    # Image rows, cols and channels
    print('(rows, cols, channels): ' + str(img.shape))
    print('Pixels: ' + str(img.shape[0] * img.shape[1]))

    # Get random centroids
    centroids = randomCentroids(img, k)

    centroidsFound = False

    while not centroidsFound:
        # Creating clusters
        print('Creating clusters...\n')
        clusters = createClusters(img, dummy, centroids)

        print('Reasigning centroids...\n')
        centroidsFound = centroidsFound or reasignCentroids(clusters, MAX_DIFF_RGB)

        newCentroids = []
        for cluster in clusters:
            newCentroids.append(cluster.centroid)
        centroids = newCentroids


    print('Making palette...\n')
    dummy[10:10 + img.shape[0], 10:10 + img.shape[1]] = img[0:img.shape[0], 0:img.shape[1]]
    sep = 10
    gaps = 0
    x = 0
    rectWidth = (img.shape[1] + 20 - (sep * (k + 1))) / k
    for cluster in clusters:
        x += sep
        xFrom = x
        xTo = x + rectWidth
        yFrom = 10 + img.shape[0] + 5
        yTo = yFrom + 25

        dummy[yFrom:yTo, xFrom:xTo] = cluster.centroid.rgb

        x = xTo

    # Do something with the result
    workImage(dummy)

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

def createClusters(img, dummy, centroids):
    clusters = []
    for centroid in centroids:
        clusters.append(clst.Cluster(centroid))

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
                dist = redDiff**2 + greenDiff**2 + blueDiff**2
                distances.append(dist)

            # Corresponding cluster
            minDistCluster = distances.index(min(distances))
            cluster = clusters[minDistCluster]

            p = point.Point(x, y, (red, green, blue))

            cluster.addPoint(p)

    return clusters

def reasignCentroids(clusters, diff):
    i = 1
    centroidsDone = 0
    for cluster in clusters:
        if cluster.centroid.alikePrev(diff):
            centroidsDone += 1
            continue
        print('Reasigning in cluster ' + str(i) + '...')
        print('Previous centroid: ' + str(cluster.centroid))
        print('Points to check: ' + str(len(cluster.points)))

        j = 0
        redSum = 0
        greenSum = 0
        blueSum = 0
        for pi in cluster.points:
            redSum += pi.red
            greenSum += pi.green
            blueSum += pi.blue

            percent = j * 100 / float(len(cluster.points))
            remPoints = len(cluster.points) - j
            sys.stdout.write("Remaning points: %d - %.2f%%\r" % (remPoints, percent) )
            sys.stdout.flush()

            j += 1

        redAverage = redSum / j
        greenAverage = greenSum / j
        blueAverage = blueSum / j

        newCentroidRGB = (redAverage, greenAverage, blueAverage)

        prevCentroid = cluster.centroid
        cluster.centroid = centroid.Centroid(0, 0, newCentroidRGB)
        cluster.centroid.prev = prevCentroid
        print('New centroid: ' + str(cluster.centroid) + '\n')
        i += 1

    return centroidsDone == len(clusters)

def workImage(img):
    if sys.argv[3] == 'sv':
        # Saving image
        cv.imwrite(str(sys.argv[4]) + '.png' or 'res.png', img)
    elif sys.argv[3] == 'sh':
        # Displaying image
        cv.imshow('image', dummy)
        print('Press any key to exit...')
        cv.waitKey(0)
        cv.destroyAllWindows()

main()
