import numpy as np
import cv2
import XuLy
import KyTu
import XacDinhKyTu
import BienSo
import math

DO_RONG_THEM=1.8
DO_CAO_THEM=1.5

MAX_GOC_LECH, MIN_GOC_LECH = 30,-30
MAX_TYLE, MIN_TYLE = 1.5,0.5
MAX_GIAONHAU, MIN_GIAONHAU =  1.0,0.8

def TimBienSo(imgGoc):
    listRawBienSo=[]
    imgXam, imgThresh=XuLy.XuLy(imgGoc)
    listKyTu=TimListKyTu(imgThresh)
    listKyTu.sort(key=lambda KyTu: KyTu.xCenter)
    listListKyTuGanNhau=XacDinhKyTu.timListListKyTuGanNhau(listKyTu)
    for listKyTuGanNhau in listListKyTuGanNhau:
        bienSo=TachBienSo(listKyTuGanNhau)
        listRawBienSo.append(bienSo)
    listBienSo=NhomBienSo(imgGoc,listRawBienSo)
    return listBienSo

def TimListKyTu(imgThresh):
    listKyTu=[]
    imgThreshCopy=imgThresh.copy()
    contours,_=cv2.findContours(imgThreshCopy,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for i in range(0,len(contours)):
        kyTu=KyTu.KyTu(contours[i])
        if kyTu.check():
            listKyTu.append(kyTu)
    return listKyTu

def TachBienSo(listKyTuGanNhau):
    bienSo=BienSo.BienSo()
    listKyTuGanNhau.sort(key=lambda KyTu: KyTu.xCenter)
    xCenterBienSo=(listKyTuGanNhau[0].xCenter+listKyTuGanNhau[len(listKyTuGanNhau)-1].xCenter)/2
    yCenterBienSo=(listKyTuGanNhau[0].yCenter+listKyTuGanNhau[len(listKyTuGanNhau)-1].yCenter)/2
    centerBienSo=xCenterBienSo,yCenterBienSo
    widthBienSo=int((listKyTuGanNhau[len(listKyTuGanNhau)-1].x+listKyTuGanNhau[len(listKyTuGanNhau)-1].width-listKyTuGanNhau[0].x)*DO_RONG_THEM)
    tongHeight=0
    for kyTu in listKyTuGanNhau:
        tongHeight=tongHeight+kyTu.height
    heightTrungBinh=tongHeight/len(listKyTuGanNhau)
    heightBienSo=int(heightTrungBinh*DO_CAO_THEM)
    canhDoi=listKyTuGanNhau[len(listKyTuGanNhau)-1].yCenter-listKyTuGanNhau[0].yCenter
    canhHuyen=XacDinhKyTu.khoangCachKyTu(listKyTuGanNhau[0],listKyTuGanNhau[len(listKyTuGanNhau)-1])
    gocRad=math.asin(canhDoi/canhHuyen)
    gocDo=gocRad*(180/math.pi)
    bienSo.thongTinViTri=(tuple(centerBienSo), (widthBienSo,heightBienSo), gocDo)
    return bienSo

import shapely.geometry
import shapely.affinity
class HinhChuNhat:
    def __init__(self, cx, cy, w, h, goc):
        self.cx=cx
        self.cy=cy
        self.w=w
        self.h=h
        self.goc=goc
    def veHinh(self):
        w=self.w
        h=self.h
        c=shapely.geometry.box(-w/2.0,-h/2.0,w/2.0,h/2.0)
        rc=shapely.affinity.rotate(c,self.goc)
        return shapely.affinity.translate(rc,self.cx,self.cy)
    def phanGiaoNhau(self, other):
        return self.veHinh().intersection(other.veHinh())

def NhomBienSo(imgGoc, listBienSo):
    biLap=set([])
    for i,value in enumerate(listBienSo):
        for j in range(i):
            if i==j: continue
            (center1, (width1, height1), goc1)=listBienSo[i].thongTinViTri
            (center2, (width2, height2), goc2)=listBienSo[j].thongTinViTri
            tyLeKhoangCach=math.sqrt((center1[0]-center2[0])**2+(center1[1]-center2[1])**2)/height1
            tyLeHeight=height2/height1
            gocLech=goc2-goc1
            if (tyLeKhoangCach<MAX_TYLE and tyLeKhoangCach>MIN_TYLE and tyLeHeight<MAX_TYLE and tyLeHeight>MIN_TYLE and
                gocLech<MAX_GOC_LECH and gocLech>MIN_GOC_LECH):
                cn1=HinhChuNhat(center1[0],center1[1],width1,height1,goc1)
                cn2=HinhChuNhat(center2[0],center2[1],width2,height2,goc2)
                dtich1=cn1.veHinh().area
                dtich2=cn2.veHinh().area
                dtichGiaoNhau=cn1.phanGiaoNhau(cn2).area
                tyLeDtich1=dtichGiaoNhau/dtich1
                tyLeDtich2=dtichGiaoNhau/dtich2
                if (tyLeDtich1<MAX_GIAONHAU and tyLeDtich1>MIN_GIAONHAU) and (tyLeDtich2<MAX_TYLE and tyLeDtich2>MIN_TYLE):
                    if dtich1<dtich2:
                        biLap.add(i)
                        break
                    else:
                        biLap.add(j)
                        continue
                if dtichGiaoNhau>0:
                    centerNhom=((center1[0]+center2[0])/2,(center1[1]+center2[1])/2)
                    widthNhom=width1 if width1>width2 else width2
                    heightNhom=height1+height2
                    gocNhom=(goc1+goc2)/2
                    listBienSo[i].co2Hang=listBienSo[j].co2Hang=True
                    listBienSo[i].thongTinViTri=(centerNhom,(widthNhom,heightNhom),gocNhom)
                    biLap.add(j)
                    break
    listBS=[]
    for i, bienso in enumerate(listBienSo):
        if i not in list(biLap) and bienso.co2Hang:
            bienSoCoAnh=TachAnh(imgGoc, bienso)
            if bienSoCoAnh.imgBienSo is not None:
                listBS.append(bienSoCoAnh)
    return listBS

def TachAnh(imgGoc, bienSo):
    centerBS, (widthBS, heightBS), gocBS = bienSo.thongTinViTri
    rotationsMatrix=cv2.getRotationMatrix2D(centerBS, gocBS, 1.0)
    width, height, _ = imgGoc.shape
    imgXoay=cv2.warpAffine(imgGoc, rotationsMatrix,(height,width))
    imgCat=cv2.getRectSubPix(imgXoay,(widthBS,heightBS),centerBS)
    bienSo.imgBienSo=imgCat
    return bienSo
