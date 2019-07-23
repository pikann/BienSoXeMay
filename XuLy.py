import cv2
import numpy as np
def XuLy(imgGoc):
    imgXam=TachValue(imgGoc)
    imgLamMo=cv2.GaussianBlur(imgXam, (5, 5), 0)
    imgThresh=cv2.adaptiveThreshold(imgLamMo, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19,9)
    return imgXam, imgThresh

def TachValue(imgGoc):
    imgHSV=cv2.cvtColor(imgGoc,cv2.COLOR_BGR2HSV)
    _,_,value=cv2.split(imgHSV)
    return value
