import math
import pygame as game
from pygame.math import Vector2
import time
from playerClass import *
from Classes import *

class Zombie:
    def __init__(self, pos, slower, instances, cam):
        self.player = instances[-1]
        self.vel = self.player.vel / slower
        self.pos = pos
        self.instances = instances
        self.win = game.display.get_surface()
        self.cam = cam

        #properties
        self.OImage = game.transform.scale(game.image.load("Images/zombie.png"), (70, 70))
        dir = [abs(self.player.pos[0] - self.pos[0]),
               abs(self.player.pos[0] - self.pos[0])]
        self.dirAngle = math.degrees(math.atan2(dir[1], dir[0]))
        self.image = game.transform.rotate(self.OImage, -self.dirAngle)
        self.imagerect = self.image.get_rect(center = self.pos)

        #health
        self.life = 3
        self.MaxHealth = self.life

    def CheckCol(self):
        pass
    def DrawMe(self):
        game.draw.rect(self.win, (255, 0, 100), self.imagerect)

    def update(self):
        if(int(self.player.pos[0]) > int(self.pos[0])):
            self.pos[0] += self.vel
        elif(int(self.player.pos[0]) < int(self.pos[0])):
            self.pos[0] -= self.vel
        if(int(self.player.pos[1]) > int(self.pos[1])):
            self.pos[1] += self.vel
        elif(int(self.player.pos[1]) < int(self.pos[1])):
            self.pos[1] -= self.vel

        dir = [self.player.pos[0] - self.pos[0],
               self.player.pos[1] - self.pos[1]]
        self.dirAngle = math.degrees(math.atan2(dir[1], dir[0])) + 90
        self.image = game.transform.rotate(self.OImage, -self.dirAngle)
        self.imagerect = self.image.get_rect(center = self.pos)


    def draw(self):
        imagerect = self.imagerect
        imagerect[0] += self.cam[0]
        imagerect[1] += self.cam[1]
        #self.win.blit(self.myimage, self.imagerect)
        #print(self.life / self.MaxHealth)
        rect = self.OImage.get_rect()
        game.draw.rect(self.win, (255, 0, 0,), (self.pos[0] - rect[2] / 2 + self.cam[0],
                                                self.pos[1] - rect[3] / 2 - rect[3] / 5 + self.cam[1],
                                                rect[2], rect[3] / 10))
        game.draw.rect(self.win, (0, 255, 0), (self.pos[0] - rect[2] / 2 + self.cam[0],
                                                self.pos[1] - rect[3] / 2 - rect[3] / 5 + self.cam[1],
                                                rect[2] - rect[2] * (self.MaxHealth - self.life) / self.MaxHealth,
                                                rect[3] / 10))
        self.win.blit(self.image, imagerect)
