import math
import pygame as game
from pygame.math import Vector2
import time
import playerClass
import zombieClass
import opstacleClass
import Classes
import settings

class Bullet:
    def __init__(self, vel):
        self.pos = settings.player.bulletSpawn
        self.win = game.display.get_surface()

        #object properties
        size = (game.image.load("Images/PeterPanV3.png").get_rect()[2], game.image.load("Images/PeterPanV3.png").get_rect()[3])
        self.OriginalImage = game.transform.scale(game.image.load("Images/PeterPanV3.png"), (int(size[0] * 0.6), int(size[1] * 0.6)))
        self.image = game.transform.rotate(self.OriginalImage, -settings.player.dirAngle).convert_alpha()
        self.imagerect = self.image.get_rect(center = self.pos)
        self.mask = game.mask.from_surface(self.image)
        self.velVector = [vel * math.cos(math.radians(settings.player.dirAngle)),
                          vel * math.sin(math.radians(settings.player.dirAngle))]
        #hitbox
        self.HitBoxSize = Vector2(self.imagerect[2] * 0.9, self.imagerect[3] * 0.9)
        self.HitTargets = [opstacleClass.Opstacle]
        self.DamageTargets = [zombieClass.Zombie]

    def update(self):
        self.pos[0] += self.velVector[0]
        self.pos[1] += self.velVector[1]
        self.imagerect.center = self.pos

        if(self.pos[0] > 5000 + settings.player.pos[0] or self.pos[0] < -5000 + settings.player.pos[0]
           or self.pos[1] > 5000 + settings.player.pos[1] or self.pos[1] < -5000 + settings.player.pos[1]):
            settings.deleteMe.append(self)
            #settings.instances.remove(self)

        col = self.CheckCol()
        if(type(col) in self.HitTargets or type(col) in self.DamageTargets):
            settings.deleteMe.append(self)
            if(type(col) in self.DamageTargets):
                col.HP -= settings.bulletDamage
                if(col.HP <= 0):
                    col.HP = 0

    def CheckCol(self):
        col = None
        for i in settings.instances:
            try:
                res = self.mask.overlap(i.mask, [int((i.pos[0] - i.imagerect[2] / 2) - (self.pos[0] - self.imagerect[2] / 2)),
                                                 int((i.pos[1] - i.imagerect[3] / 2) - (self.pos[1] - self.imagerect[3] / 2))])
                if(res != None):
                    col = i
            except:
                pass
        return col

    def draw(self):
        imagerect = self.imagerect
        imagerect[0] += settings.CameraPos[0]
        imagerect[1] += settings.CameraPos[1]
        self.win.blit(self.image, imagerect)
    def DrawMe(self):
        game.draw.rect(self.win, (255, 0, 0), (self.imagerect[0] + settings.CameraPos[0], self.imagerect[1] + settings.CameraPos[1], self.imagerect[2], self.imagerect[3]))
        game.draw.rect(self.win, (0, 255, 255), (self.pos[0] - self.HitBoxSize[0] / 2 + settings.CameraPos[0],
                                                 self.pos[1] - self.HitBoxSize[1] / 2 + settings.CameraPos[1],
                                                 self.HitBoxSize[0], self.HitBoxSize[1]))
        game.draw.circle(self.win, (0, 255, 0), [int(self.pos[0] + settings.CameraPos[0]), int(self.pos[1] + settings.CameraPos[1])], 10)

class Flash:
    def __init__(self, win, surviveTime):
        self.win = win
        self.pos = settings.player.bulletSpawn

        #time
        self.surviveTime = surviveTime
        self.t = time.time()

        #image
        size = (game.image.load("Images/muzzleFlash.png").get_rect()[2], game.image.load("Images/muzzleFlash.png").get_rect()[3])
        self.OriginalImage = game.transform.scale(game.image.load("Images/muzzleFlash.png"), (int(size[0] * 0.4), int(size[1] * 0.4)))
        self.image = game.transform.rotate(self.OriginalImage, -settings.player.dirAngle)
        self.imagerect = self.image.get_rect(center = self.pos)

    def update(self):
        if(time.time() - self.t > self.surviveTime):
            settings.deleteMe.append(self)
            #settings.instances.remove(self)

    def DrawMe(self):
        pass

    def draw(self):
        self.win.blit(self.image, (self.imagerect[0] + settings.CameraPos[0], self.imagerect[1] + settings.CameraPos[1], self.imagerect[2], self.imagerect[3]))
