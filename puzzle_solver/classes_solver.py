"""
Created on Sun Feb 14 16:04:11 2021

@author: Hana
"""

class PuzzlePiece:
    def _init_(self):
        self.image=[]
        self.mask=[]
        self.corners=[]
        self.edges_solver=[Edge_S(),Edge_S(),Edge_S(),Edge_S()]

class Edge_S:
    def _init_(self):
        self.points
        self.act_length
        self.straight_length
        self.type
