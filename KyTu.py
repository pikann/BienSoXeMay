import cv2
import math
MIN_S=30
MIN_WIDTH=2
MIN_HEIGHT=8
MIN_TYLE=0.15
MAX_TYLE=1.0
class KyTu:
    def __init__(self, _contour):
        self.contour=_contour
        self.laKyTu=True
        self.boundingRect=cv2.boundingRect(self.contour)
        [self.x, self.y, self.width, self.height]=self.boundingRect
        self.rectS=self.width*self.height
        self.xCenter=self.x+self.width/2
        self.yCenter=self.y+self.height/2
        self.duongCheo=math.sqrt(self.width**2+self.height**2)
        self.tyLe=float(self.width)/float(self.height)
    def check(self):
        if (self.rectS>MIN_S and self.width>MIN_WIDTH and self.height>MIN_HEIGHT and
            self.tyLe>MIN_TYLE and self.tyLe<MAX_TYLE):
            return True
        else: return False
