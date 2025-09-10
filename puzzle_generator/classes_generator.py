"""
Created on Mon Oct 26 14:49:55 2020

@author: Hana
"""
import numpy as np
from matplotlib import pyplot as plt

class PuzzlePiece:
    def _init_(self):
        self.centre=np.zeros((1,2))
        self.coordx= np.zeros((4,2))
        self.coordy= np.zeros((4,2))
        self.e=[Edge(),Edge(),Edge(),Edge()]
        self.alledges=[Edge(),Edge(),Edge(),Edge()]
        self.image=[]

    def plot(self):
        for i in range(4):
            self.alledges[i].plot()

class Edge:
    def _init_(self):
        self.guidepoints=[]
        self.points=np.zeros([2,2])

    def plot(self):
        plt.plot(self.points[:,0],self.points[:,1],'b')
