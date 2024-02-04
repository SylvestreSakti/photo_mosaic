import numpy as np
import cv2
import os
import glob
import random
import copy

from Tile import Tile
from Mosaic import Mosaic

class Optimizer :

    def __init__(self,tiles : list, mosaic : Mosaic):
        self.tiles = tiles
        self.mosaic = mosaic
        for i in range(self.mosaic.height):
            for j in range(self.mosaic.width):
                self.mosaic.setTile(random.choice(self.tiles), i, j)


    def fill(self,steps):
        for step in range(steps) :
            for i in range(self.mosaic.height) :
                for j in range(self.mosaic.width) :
                    selection = copy.deepcopy(random.choice(self.tiles))
                    selection.setOffset(random.randrange(-150,30))
                    print(self.mosaic.updateTile(selection,i,j))
        self.mosaic.computeMosaic()


tiles = []
for file in glob.iglob("C:/Users/laksh/Desktop/Nouveau dossier (2)/"+"*.jpg"):
    tiles.append(Tile(os.path.abspath(file)))

test = Tile("C:/Users/laksh/Desktop/Fontainebleau/_DSC0005.JPG")

#cv2.waitKey(0)
testMos = Mosaic("C:/Users/laksh/Desktop/milou.jpg",14)
testMos.setTile(test,2,1)

optimizer = Optimizer(tiles,testMos)
for i in range(20) :
    optimizer.fill(10)
    testMos.showGrid()
    testMos.showGridResult()
    testMos.showMosaic()
    cv2.waitKey(2)
cv2.waitKey(0)