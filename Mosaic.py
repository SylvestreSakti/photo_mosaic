import numpy as np
import cv2
import os
import glob

from Tile import Tile

class Mosaic :

    def __init__(self,path,tileRes):
        self.image = np.clip(cv2.imread(path,cv2.IMREAD_GRAYSCALE),2,200).astype(np.uint8)
        self.tileRes = tileRes
        self.height = int(self.image.shape[0] / tileRes)
        self.width = int(self.image.shape[1]/tileRes)
        self.mosGrid = []
        self.mosGridResult = []
        self.mosTiles = []
        for i in range(self.height) :
            self.mosGrid.append([])
            self.mosGridResult.append([])
            self.mosTiles.append([])
            for j in range(self.width) :
                self.mosGrid[i].append(np.zeros([Tile.grid_res, Tile.grid_res], np.uint16))
                self.mosGridResult[i].append(np.zeros([Tile.grid_res, Tile.grid_res], np.uint16))
                self.mosTiles[i].append([])
        self.computeGrid()

    def computeGrid(self):
        step = int(self.tileRes / Tile.grid_res)
        for i in range(self.height):
            for j in range(self.width):
                cell = self.image[i*self.tileRes:(i+1) * self.tileRes, j*self.tileRes:(j+1)*self.tileRes]
                for i1 in range(Tile.grid_res):
                    for j1 in range(Tile.grid_res):
                        self.mosGrid[i][j][i1, j1] = np.uint16(np.average(cell[i1 * step:(i1 + 1) * step, j1 * step:(j1 + 1) * step]))

    def showGrid(self):
        step = int(self.tileRes / Tile.grid_res)
        img = np.zeros([self.tileRes*self.height,self.tileRes*self.width],np.uint8)
        for i in range(self.height):
            for j in range(self.width):
                for i1 in range(self.tileRes) :
                    for j1 in range(self.tileRes):
                        img[i*self.tileRes+i1,j*self.tileRes+j1] = self.mosGrid[i][j][min(int(i1/step),Tile.grid_res-1),min(int(j1/step),Tile.grid_res-1)]
        cv2.imshow("Grid",img)

    def showGridResult(self):
        step = int(self.tileRes / Tile.grid_res)
        img = np.zeros([self.tileRes*self.height,self.tileRes*self.width],np.uint8)
        for i in range(self.height):
            for j in range(self.width):
                for i1 in range(self.tileRes) :
                    for j1 in range(self.tileRes):
                        img[i*self.tileRes+i1,j*self.tileRes+j1] = self.mosGridResult[i][j][min(int(i1/step),Tile.grid_res-1),min(int(j1/step),Tile.grid_res-1)]
        cv2.imshow("Grid Result",img)

    def showMosaic(self):
        lineImg = [cv2.hconcat([t.processedImg for t in self.mosTiles[0]])]
        for i in range(1,self.height):
            lineImg += [cv2.hconcat([t.processedImg for t in self.mosTiles[i]])]
        fullImg = cv2.vconcat(lineImg)
        cv2.imshow("Mosaic Result", fullImg)
        cv2.imwrite("result.bmp",fullImg)

    def setTile(self,tile:Tile,i,j):
        self.mosTiles[i][j] = tile
        self.mosGridResult[i][j] = tile.grid

    def updateTile(self,tile:Tile,i,j):
        score = np.average(np.abs(self.mosGridResult[i][j]-tile.grid))
        if(np.average(np.abs(self.mosGrid[i][j]-tile.grid)) > np.average(np.abs(self.mosGrid[i][j]- self.mosTiles[i][j].grid))) :
            self.mosTiles[i][j] = tile
            self.mosGridResult[i][j] = np.copy(tile.grid)
        return np.average(np.abs(self.mosGridResult[i][j]- self.mosGrid[i][j]))

    def computeMosaic(self):
        for i in range(self.height):
            for j in range(self.width):
                self.mosTiles[i][j].computeProcessedImg()
