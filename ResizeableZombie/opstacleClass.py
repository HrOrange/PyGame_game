import math
import pygame as game
from pygame.math import Vector2
import time
import playerClass
import zombieClass
import settings

class Opstacle:
    def __init__(self, pos, block):
        self.pos = pos
        self.block = block
        self.win = game.display.get_surface()
        self.OriginalImage = game.transform.scale(game.image.load("Images/WoodenBox.png"), (60, 60)).convert_alpha()
        self.imagerect = self.OriginalImage.get_rect(center = self.pos)
        self.mask = game.mask.from_surface(self.OriginalImage)

    def CheckCol(self):
        pass
    def update(self):
        pass

    def DrawMe(self):
        game.draw.circle(self.win, (0, 0, 255), [int(self.pos[0] + settings.CameraPos[0]), int(self.pos[1] + settings.CameraPos[1])], 10)

    def draw(self):
        self.win.blit(self.OriginalImage, (self.imagerect[0] + settings.CameraPos[0], self.imagerect[1] + settings.CameraPos[1], self.imagerect[2], self.imagerect[3]))
        #game.draw.circle(self.win, (255, 0, 255), [int(self.pos[0] + self.imagerect[2] / 2), int(self.pos[1] + self.imagerect[3] / 2)], 15)
