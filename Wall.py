import pygame
from Player import Player
import math

class Wall:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.clamp_x = 0
        self.clamp_y = 0
        self.distance = 0

    def clamp(self, min, max, value):
        if value<min:
            return min
        elif value>max:
            return max
        else:
            return value

    def isCollidingCircle(self, player):
        r = 15
        self.clamp_x = self.clamp(self.x, self.x+self.w, player.x)
        self.clamp_y = self.clamp(self.y, self.y+self.h, player.y)
        w = [self.clamp_x, self.clamp_y]
        p2 = [player.x,player.y]
        self.distance = math.dist(w,p2)
        if round(self.distance) == 0:
            self.distance = 1
        if self.distance < 15:
            return True
        else:
            return False

    def isCollidingRect(self, player):
        self.left = self.x +self.w - player.x
        self.right = player.x+30 - self.x
        self.top = self.y +self.h - player.y
        self.bottom = player.y + 30 - self.y
        if self.left > 0 and self.right>0 and self.top >0 and self.bottom>0:
            return True
        else:
            return False
