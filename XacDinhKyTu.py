import math
import XuLy
import cv2
import XacDinhBienSo

MAX_TYLE_KHOANGCACH=3.2
MAX_GOCLECH=15
MAX_DOLECH_S=0.4
MAX_DOLECH_WIDTH=0.6
MAX_DOLECH_HEIGHT=0.2

MIN_KYTU=2

def xacDinhKyTu(listBienSo):
    if len(listBienSo)==0: return listBienSo
    for i, bienSo in enumerate(listBienSo):
        bienSo.imgXam, bienSo.imgThresh = XuLy.XuLy(bienSo.imgBienSo)
        adaptive=cv2.adaptiveThreshold(bienSo.imgXam,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)
        bienSo.imgThresh=cv2.resize(bienSo.imgThresh,(0,0), fx=1.6, fy=1.6)
        listKyTu=XacDinhBienSo.TimListKyTu(adaptive)
        listKyTu.sort(key=lambda KyTu: KyTu.xCenter)
        listListKyTuGanNhau=timListListKyTuGanNhau(listKyTu, minKyTu=3, maxGoc=10)
        if len(listListKyTuGanNhau)==0: continue

        listListKyTu1=[timListCungHeight(x) for x in listListKyTuGanNhau]
        listListKyTu1.sort(key=lambda ListKyTu: ListKyTu[0].yCenter)
        for listKyTuXep in listListKyTu1:
            listKyTuXep.sort(key=lambda KyTu: KyTu.xCenter)
        listListKyTu1=[x for x in listListKyTu1 if len(x)>0]
        listListKyTu2=timListCungHeight(listListKyTu1,mode=1)
        listListKyTu3=[timListKeSatNhau(x) for x in listListKyTu2]
        listKyTuCuoi=[kyTu for listKyTu1 in listListKyTu3 for kyTu in listKyTu1]
        listKyTuCuoi=xoaKyTuBenTrong(listKyTuCuoi)
        if len(listKyTuCuoi)>=6:
            bienSo.laBienSo=True
            bienSo.xauKyTu=xuLyKiTu(bienSo.imgXam,listKyTuCuoi)
    listBienSoCuoi=[bienSo for bienSo in listBienSo if bienSo.laBienSo]
    return listBienSoCuoi


def timListListKyTuGanNhau(listKyTu,minKyTu=MIN_KYTU,maxGoc=MAX_GOCLECH):
    listListKyTuGanNhau=[]
    for kyTu in listKyTu:
        listKyTuGan=timListKyTuGan(kyTu, listKyTu, maxGoc)
        listKyTuGan.append(kyTu)
        if len(listKyTuGan)<minKyTu: continue
        listListKyTuGanNhau.append(listKyTuGan)
        listKyTuChuaXet=list(set(listKyTu)-set(listKyTuGan))
        listLishKyTuGanNhauKhac=timListListKyTuGanNhau(listKyTuChuaXet)
        for listKyTuGanNhauKhac in listLishKyTuGanNhauKhac:
            listListKyTuGanNhau.append(listKyTuGanNhauKhac)
        break
    return listListKyTuGanNhau


def timListKyTuGan(kyTu, listKyTu, maxGoc=MAX_GOCLECH):
    listKyTuGan=[]
    for kyTuGan in listKyTu:
        if kyTuGan==kyTu: continue
        khoangCach=khoangCachKyTu(kyTu,kyTuGan)
        gocLech=gocLechKyTu(kyTu,kyTuGan)
        doLechS=float(abs(kyTuGan.rectS-kyTu.rectS))/float(kyTu.rectS)
        doLechWidth=float(abs(kyTuGan.width-kyTu.width))/float(kyTu.width)
        doLechHeight=float(abs(kyTuGan.height-kyTu.height))/float(kyTu.height)
        if (khoangCach<(kyTu.duongCheo*MAX_TYLE_KHOANGCACH) and
            gocLech<maxGoc and
            doLechS<MAX_DOLECH_S and
            doLechWidth<MAX_DOLECH_WIDTH and
            doLechHeight<MAX_DOLECH_HEIGHT):
            listKyTuGan.append(kyTuGan)
    return listKyTuGan


def khoangCachKyTu(kyTu1, kyTu2):
    khoangCachX=abs(kyTu1.xCenter-kyTu2.xCenter)
    khoangCachY=abs(kyTu1.yCenter-kyTu2.yCenter)
    return math.sqrt(khoangCachX**2+khoangCachY**2)

def gocLechKyTu(kyTu1, kyTu2):
    khoangCachX = float(abs(kyTu1.xCenter - kyTu2.xCenter))
    khoangCachY = float(abs(kyTu1.yCenter - kyTu2.yCenter))
    if khoangCachX!=0:
        gocRad=math.atan(khoangCachY/khoangCachX)
    else:
        gocRad=math.pi/2
    gocDo=gocRad*(180.0/math.pi)
    return gocDo

import numpy as np

def khoangSaiSo(listHeight):
    m=np.median(listHeight)
    std=np.std(listHeight)
    tyle=std/m
    n=[1,3][tyle<0.05]
    return m+n*std,m-n*std

def timListCungHeight(listKyTu, mode=0):
    if mode:
        listHeight=[x[0].height for x in listKyTu]
    else:
        listHeight=[x.height for x in listKyTu]
    khoangTren, khoangDuoi = khoangSaiSo(listHeight)
    if mode:
        listKyTu=[x for x in listKyTu if x[0].height>=khoangDuoi and x[0].height<=khoangTren]
    else:
        listKyTu=[x for x in listKyTu if x.height>=khoangDuoi and x.height<=khoangTren]
    return listKyTu

def timListKeSatNhau(listKyTu):
    for i, kyTu1 in enumerate(listKyTu):
        keSat=False
        for j, kyTu2 in enumerate(listKyTu):
            tyLeKhoangCach=math.sqrt((kyTu1.xCenter-kyTu2.xCenter)**2+(kyTu1.yCenter-kyTu2.yCenter)**2)/kyTu1.duongCheo
            if tyLeKhoangCach>0 and tyLeKhoangCach<1:
                keSat=True
        if not keSat: kyTu1.laKyTu=False
    listKyTu1=[kyTu for kyTu in listKyTu if kyTu.laKyTu==True]
    return listKyTu1

def xoaKyTuBenTrong(listKyTu):
    for i, kyTu1 in enumerate(listKyTu):
        for j, kyTu2 in enumerate(listKyTu):
            dau_x1, dau_y1 = kyTu1.x, kyTu1.y
            cuoi_x1, cuoi_y1 = kyTu1.x+kyTu1.width, kyTu1.y+kyTu1.height
            dau_x2, dau_y2 = kyTu2.x, kyTu2.y
            cuoi_x2, cuoi_y2 = kyTu2.x+kyTu2.width, kyTu2.y+kyTu2.height
            if dau_x1<dau_x2 and cuoi_x1>cuoi_x2 and dau_y1<dau_y2 and cuoi_y1>cuoi_y2:
                kyTu2.laKyTu=False
    listKyTuCuoi=[kyTu for kyTu in listKyTu if kyTu.laKyTu==True]
    return listKyTuCuoi

import tensorflow as tf

def duDoanKyTu(anhKyTu):
    tapKyTu=["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H",
           "K","L","M","N","P","R","S","T","U","V","X","Y","Z"]
    model=tf.keras.models.load_model('model.h5')
    kyTus=""
    for anh in anhKyTu:
        anh=tf.reshape(anh,shape=[1,28,12,1])
        predictions=model.predict(anh,steps=1)
        kyTu=np.argmax(predictions[0])
        kyTus=kyTus+tapKyTu[kyTu]
    return kyTus

def xuLyKiTu(imgXam, listKyTu):
    anhKyTu=[]
    for i, kyTu in enumerate(listKyTu):
        pt1=(kyTu.x,kyTu.y)
        pt2=((kyTu.x+kyTu.width),(kyTu.y+kyTu.height))
        imgKyTu=imgXam[pt1[1]:pt2[1],pt1[0]:pt2[0]]
        imgKyTuResized=cv2.resize(imgKyTu, (12,28))
        ret, im = cv2.threshold(imgKyTuResized, 150, 255, cv2.THRESH_BINARY)
        im=cv2.bitwise_not(im)
        anhKyTu.append(im)
    kyTus=duDoanKyTu(anhKyTu)
    return kyTus