import numpy as np
import cv2 as cv
import sys
from random import randint
import centroid
import cluster as clst
import point
import argparse

def defineArgs():
    parser = argparse.ArgumentParser(
        description='simple script to find dominant colors in an image'
    )

    parser.add_argument('image', help='the image to process')

    parser.add_argument(
        '-k',
        help='number of means to search',
        type=int,
        default=3,
    )

    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        '-o', '--output',
        help='save palette in specified route',
        default='output',
    )

    action.add_argument(
        '-s', '--show',
        help='show palette on screen',
        action='store_true'
    )

    parser.add_argument(
        '-d', '--diff',
        help='max difference between RGB values to tell if mean is correct',
        type=int,
        default=5
    )

    parser.add_argument(
        '-r', '--resize',
        help='number of pixels of image to process',
        type=int,
        default=500
    )

    return parser.parse_args()

def main(args):

    # Reading image
    toProcess = cv.imread(args.image)
    original = cv.imread(args.image)

    # If the image is too large, resize
    if toProcess.shape[0] > args.resize or toProcess.shape[1] > args.resize:
        toProcess = resize(toProcess, args.resize)

    # Resulting image
    result = np.zeros((original.shape[0] + 50, original.shape[1] + 20, 3), np.uint8)
    # Make white
    result[0:original.shape[0] + 50, 0:original.shape[1] + 20] = (255, 255, 255)

    # k-means
    k = args.k

    # Max difference between RGB values to tell if the found mean is correct
    diff = args.diff

    # Image rows, cols and channels
    print('(rows, cols, channels): ' + str(toProcess.shape))
    print('Pixels: ' + str(toProcess.shape[0] * toProcess.shape[1]))

    # Get random centroids
    centroids = randomCentroids(toProcess, k)

    centroidsFound = False

    while not centroidsFound:
        # Creating clusters
        print('Creating clusters...\n')
        clusters = createClusters(toProcess, centroids)

        print('Reasigning centroids...\n')
        centroidsFound = centroidsFound or reasignCentroids(clusters, diff)

        newCentroids = []
        for cluster in clusters:
            newCentroids.append(cluster.centroid)
        centroids = newCentroids


    print('Making palette...\n')
    result[10:10 + original.shape[0], 10:10 + original.shape[1]] = original[0:original.shape[0], 0:original.shape[1]]
    sep = 10
    gaps = 0
    x = 0
    rectWidth = (original.shape[1] + 20 - (sep * (k + 1))) / k
    for cluster in clusters:
        x += sep
        xFrom = x
        xTo = x + rectWidth
        yFrom = 10 + original.shape[0] + 5
        yTo = yFrom + 25

        result[yFrom:yTo, xFrom:xTo] = cluster.centroid.rgb

        x = xTo

    # Do something with the result
    workImage(result, args)

def resize(img, desiredDim):
    dimensions = (img.shape[0], img.shape[1])
    biggest = max(dimensions)
    smallest = min(dimensions)

    ratio = smallest / float(biggest)

    difference = biggest - desiredDim

    toSubstract = difference * ratio

    newSize = (biggest - difference, int(smallest - toSubstract))

    print('Image resized from ' + str(dimensions) + ' to ' + str(newSize))
    savedPixels = (dimensions[0] * dimensions[1]) - (newSize[0] * newSize[1])
    print('Saved pixels: ' + str(savedPixels))

    return cv.resize(img, newSize)

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

def createClusters(img, centroids):
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

        # Division by zero is possible, if there no exists any
        # points for that cluster
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

def workImage(img, args):
    if args.show is False:
        # Saving image
        cv.imwrite(args.output + '.png', img)
    else:
        # Displaying image
        cv.imshow('image', img)
        print('Press any key to exit...')
        cv.waitKey(0)
        cv.destroyAllWindows()

main(defineArgs())
