import cv2
import numpy as np
import XuLy
import XacDinhBienSo
import XacDinhKyTu
import random

img=cv2.imread("tra-cuu-chu-so-huu-bien-so-xe-may.jpg", 1)
cv2.imshow("Goc", img)
"""imgXam, imgThresh=XuLy.XuLy(img)

listKyTu=XacDinhBienSo.TimListKyTu(imgThresh)
listKyTu.sort(key=lambda Char: Char.xCenter)

height,width,_=img.shape
imgContours=np.zeros([height,width,3], np.uint8)
contours=[]
for kyTu in listKyTu:
    contours.append(kyTu.contour)
cv2.drawContours(imgContours,contours,-1,(255.0,255.0,255.0))

listListKyTuNoiNhau=XacDinhKyTu.timListListKyTuGanNhau(listKyTu)

height,width,_=img.shape
imgContours2=np.zeros([height,width,3], np.uint8)
for listKyTuNoiNhau in listListKyTuNoiNhau:
    contours=[]
    for kyTu in listKyTuNoiNhau:
        contours.append(kyTu.contour)
    cv2.drawContours(imgContours2,contours,-1,(random.randint(0,255),
                                               random.randint(0,255),
                                               random.randint(0,255)))

cv2.imshow("Xam", imgXam)
cv2.imshow("Thresh", imgThresh)
cv2.imshow("Contours", imgContours)
cv2.imshow("Contours2", imgContours2)"""

listBienSo=XacDinhBienSo.TimBienSo(img)
for bienSo in listBienSo:
    cv2.imshow("BienSo",bienSo.imgBienSo)
"""bsXam, bsThresh = XuLy.XuLy(listBienSo[0].imgBienSo)
bsThresh=cv2.resize(bsThresh, (0,0), fx=1.6, fy=1.6)
cv2.imshow("BSThresh", bsThresh)"""
listBienSoCuoi=XacDinhKyTu.xacDinhKyTu(listBienSo)
for bienSo in listBienSoCuoi:
    print(bienSo.xauKyTu)
cv2.waitKey(0)
cv2.destroyAllWindows()