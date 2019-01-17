import numpy as np
import cv2 as cv
import sys
from random import randint

def main():
    # Reading image
    img = cv.imread(sys.argv[1])
    k = int(sys.argv[2])
    print('k-clusters: %d' % (k))

    # Image rows, cols and channels
    print(img.shape)

    # Get random centroids
    centroids = randomCentroids(img, k)

    # Centroids coordinates
    print(centroids)

    # and their respective colors
    for centroid in centroids:
        print(img[centroid[0], centroid[1]])

    # Displaying image
    cv.imshow('image', img)
    print('Press any key to exit...')
    cv.waitKey(0)
    cv.destroyAllWindows()

def randomCentroids(img, k):
    imgRows = img.shape[0]
    imgCols = img.shape[1]

    centroids = []

    for i in range(0, k):
        centroids.append((randint(0, imgRows), randint(0, imgCols)))

    return centroids

main()
