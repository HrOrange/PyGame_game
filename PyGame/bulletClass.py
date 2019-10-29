import math
import pygame as game
from pygame.math import Vector2
import time
import playerClass
import zombieClass
import Classes

class Bullet:
    def __init__(self, vel, player, instances, cam):
        self.instances = instances
        self.player = player
        self.pos = player.bulletSpawn
        self.cam = cam
        self.win = game.display.get_surface()

        #object properties
        size = (game.image.load("Images/PeterPanV3.png").get_rect()[2], game.image.load("Images/PeterPanV3.png").get_rect()[3])
        self.OriginalImage = game.transform.scale(game.image.load("Images/PeterPanV3.png"), (int(size[0] * 0.6), int(size[1] * 0.6)))
        self.image = game.transform.rotate(self.OriginalImage, -player.dirAngle)
        self.imagerect = self.image.get_rect(center = self.pos)
        self.velVector = [abs(vel) * math.cos(math.radians(player.dirAngle)),
                          abs(vel) * math.sin(math.radians(player.dirAngle))]
        #hitbox
        self.HitBoxSize = Vector2(self.imagerect[2] * 0.9, self.imagerect[3] * 0.9)
        self.hitTargets = [zombieClass.Zombie, Classes.Opstacle]

    def update(self):
        self.pos[0] += self.velVector[0]
        self.pos[1] += self.velVector[1]
        colTrue, col = self.CheckCol()
        if(self.pos[0] > 5000 or self.pos[0] < -5000 or self.pos[1] > 5000
           or self.pos[1] < -5000 or colTrue):
            self.instances.remove(self)
            if(type(col) == zombieClass.Zombie):
                col.life -= 1
                if(col.life == 0):
                    self.instances.remove(col)
        self.imagerect.center = self.pos

    def CheckCol(self):
        hit = False
        col = None
        for i in self.instances:
            HitRight = False
            for x in self.hitTargets:
                if(type(i) == x):
                    HitRight = True
            if(HitRight and
            self.pos[1] + self.HitBoxSize[1] / 2 > i.pos[1] - i.imagerect[3] / 2 and #top
            self.pos[1] - self.HitBoxSize[1] / 2 < i.pos[1] + i.imagerect[3] / 2 and #down
            self.pos[0] + self.HitBoxSize[0] / 2 > i.pos[0] - i.imagerect[2] / 2 and #left
            self.pos[0] - self.HitBoxSize[0] / 2 < i.pos[0] + i.imagerect[2] / 2): #right
                hit = True
                col = i
        return hit, col

    def draw(self):
        imagerect = self.imagerect
        imagerect[0] += self.cam[0]
        imagerect[1] += self.cam[1]
        self.win.blit(self.image, imagerect)
    def DrawMe(self):
        imagerect = self.imagerect
        imagerect[0] += self.cam[0]
        imagerect[1] += self.cam[1]
        game.draw.rect(self.win, (255, 0, 0), imagerect)
        game.draw.rect(self.win, (0, 255, 255), (self.pos[0] - self.HitBoxSize[0] / 2 + self.cam[0],
                                                 self.pos[1] - self.HitBoxSize[1] / 2 + self.cam[1],
                                                 self.HitBoxSize[0], self.HitBoxSize[1]))
        game.draw.circle(self.win, (0, 255, 0), [int(self.pos[0] + self.cam[0]), int(self.pos[1] + self.cam[1])], 10)

class Flash:
    def __init__(self, win, instances, surviveTime, cam):
        self.win = win
        self.pos = instances[-1].bulletSpawn
        self.instances = instances
        self.cam = cam

        #time
        self.surviveTime = surviveTime
        self.t = time.time()

        #image
        size = (game.image.load("Images/muzzleFlash.png").get_rect()[2], game.image.load("Images/muzzleFlash.png").get_rect()[3])
        self.OriginalImage = game.transform.scale(game.image.load("Images/muzzleFlash.png"), (int(size[0] * 0.4), int(size[1] * 0.4)))
        self.image = game.transform.rotate(self.OriginalImage, -instances[-1].dirAngle)
        self.imagerect = self.image.get_rect(center = self.pos)

    def update(self):
        if(time.time() - self.t > self.surviveTime):
            self.instances.remove(self)

    def DrawMe(self):
        pass

    def draw(self):
        self.win.blit(self.image, self.imagerect)
