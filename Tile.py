import numpy as np
import cv2
import os

class Tile :

    res = 128
    grid_res = 2

    def __init__(self,path) :
        self.image = []
        self.processedImg = []
        self.path = path
        self.grid = np.zeros([Tile.grid_res,Tile.grid_res],np.uint16)
        self.mean = 0
        self.offset = 0
        self.open()
        self.computeGrid()
        self.computeMean()
        self.computeProcessedImg()

    def computeGrid(self):
        step = int(Tile.res/Tile.grid_res)
        for i in range(Tile.grid_res) :
            for j in range(Tile.grid_res):
                self.grid[i,j] = np.clip(int(np.average(self.image[i*step:(i+1)*step,j*step:(j+1)*step]))+self.offset,0,255)
        self.grid = self.grid.astype(np.uint16)

    def computeMean(self):
        self.mean = int(np.average(self.image))

    def computeProcessedImg(self):
        self.processedImg = np.clip(np.copy(self.image).astype(int)+self.offset,13,255).astype(np.uint8)

    def setOffset(self,offset):
        self.offset = offset
        self.computeGrid()

    def getTilePath(self):
        return os.path.splitext(self.path)[0]+"tile_"+str(Tile.res)+".bmp"

    def showImg(self):
        cv2.imshow("Rescaled Image", self.image)

    def showProcessedImg(self):
        cv2.imshow("Processed Image", self.processedImg)

    def showGrid(self):
        grid = self.grid.astype(np.uint8)
        step = int(Tile.res / Tile.grid_res)
        img = np.zeros([Tile.res,Tile.res],np.uint8)
        for i in range(step*Tile.grid_res) :
            for j in range(step*Tile.grid_res):
                img[i,j] = grid[int(i/step),int(j/step)]
        cv2.imshow("Gridded Image", img)

    def open(self):
        newPath = self.getTilePath()
        if os.path.exists(newPath) :
            self.image = cv2.imread(newPath)
        else :
            self.load()
            self.save()

    def load(self):
        img = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        height = img.shape[0]
        width = img.shape[1]
        if height < width :
            croppedImg = img[0:height,int((width-height)/2):int((width+height)/2)]
        elif width < height:
            croppedImg = img[int((height-width)/2):int((height+width)/2),0:width]
        else :
            croppedImg = img
        self.image = cv2.resize(croppedImg,[Tile.res,Tile.res])


    def save(self):
        newPath = self.getTilePath()
        cv2.imwrite(newPath,self.image)
