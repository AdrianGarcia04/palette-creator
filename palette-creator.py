import numpy as np
import cv2 as cv

def main():
    # Reading image
    img = cv.imread('rusia.png')

    # Displaying image
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

main()
