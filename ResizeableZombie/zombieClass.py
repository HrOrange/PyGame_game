import math
import pygame as game
from pygame.math import Vector2
import time
from playerClass import *
from Classes import *
import settings

class Zombie:
    def __init__(self, pos, slower):
        self.pos = pos
        self.win = game.display.get_surface()

        #health
        self.HP = random.randint(1 * settings.ZombieSize, 7 * settings.ZombieSize)
        self.vel = (240 - self.HP) / 240 * settings.ZombieSpeed
        self.MaxHP = self.HP
        self.bleedTimer = time.time()

        #properties
        self.OImage = game.transform.scale(game.image.load("Images/zombie.png"), (self.HP, self.HP))
        self.OImagerect = self.OImage.get_rect()
        dir = [abs(settings.player.pos[0] - self.pos[0]),
               abs(settings.player.pos[0] - self.pos[0])]
        self.dirAngle = math.degrees(math.atan2(dir[1], dir[0]))
        self.image = game.transform.rotate(self.OImage, -self.dirAngle).convert_alpha()
        self.imagerect = self.image.get_rect(center = self.pos)
        self.mask = game.mask.from_surface(self.image)

    def CheckCol(self):
        pass

    def DrawMe(self):
        game.draw.rect(self.win, (255, 0, 100), (self.imagerect[0] + settings.CameraPos[0], self.imagerect[1] + settings.CameraPos[1], self.imagerect[2], self.imagerect[3]))
        game.draw.rect(self.win, (255, 0, 100), (self.pos[0] - self.hitbox[0] / 2 + settings.CameraPos[0], self.pos[1] - self.hitbox[1] / 2 + settings.CameraPos[1], self.hitbox[0], self.hitbox[1]))

    def update(self):
        if(int(settings.player.pos[0]) > int(self.pos[0])):
            self.pos[0] += self.vel
        elif(int(settings.player.pos[0]) < int(self.pos[0])):
            self.pos[0] -= self.vel
        if(int(settings.player.pos[1]) > int(self.pos[1])):
            self.pos[1] += self.vel
        elif(int(settings.player.pos[1]) < int(self.pos[1])):
            self.pos[1] -= self.vel

        dir = [settings.player.pos[0] - self.pos[0],
               settings.player.pos[1] - self.pos[1]]
        self.dirAngle = math.degrees(math.atan2(dir[1], dir[0])) + 90
        self.image = game.transform.rotate(self.OImage, -self.dirAngle)
        self.imagerect = self.image.get_rect(center = self.pos)
        self.mask = game.mask.from_surface(self.image)
        self.hitbox = [self.imagerect[2] * 0.8, self.imagerect[3] * 0.8]

        if(self.HP != self.MaxHP and self.MaxHP > 150 and time.time() - self.bleedTimer > 1):
            self.HP -= 10
            self.bleedTimer = time.time()
        if(self.HP <= 0):
            self.HP = 0
            settings.ZombieCount -= 1
            settings.deleteMe.append(self)
            #settings.instances.remove(col)
            settings.score += 1
            settings.deleteMe.append(self)
            if(settings.player.MaxAmmo != settings.maxAmmo):
                if(settings.player.MaxAmmo + 4 <= settings.maxAmmo):
                    settings.player.MaxAmmo += math.floor(self.MaxHP / settings.bulletDamage) - 1
                else:
                    settings.player.MaxAmmo = settings.maxAmmo

    def draw(self):
        #self.win.blit(self.myimage, self.imagerect)
        if(self.HP != self.MaxHP):
            settings.font = game.font.Font(None, 20)
            DamageText = settings.font.render(str(self.HP) + " / " + str(self.MaxHP), True, (200, 200, 200))
            DamageTextRect = DamageText.get_rect()
            self.win.blit(DamageText,(self.pos[0] + settings.CameraPos[0] - len(str(self.HP) + " / " + str(self.MaxHP)) * 3,
                                      self.pos[1] - self.OImagerect[3] / 2 - 2 * self.OImagerect[3] / 8 - 8 + settings.CameraPos[1],
                                      DamageTextRect[2],
                                      DamageTextRect[3]))


        game.draw.rect(self.win, (255, 0, 0), (self.pos[0] - self.OImagerect[2] / 2 + settings.CameraPos[0],
                                               self.pos[1] - self.OImagerect[3] / 2 - self.OImagerect[3] / 8 + settings.CameraPos[1],
                                               self.OImagerect[2],
                                               self.OImagerect[3] / 8))
        game.draw.rect(self.win, (0, 255, 0), (self.pos[0] - self.OImagerect[2] / 2 + settings.CameraPos[0],
                                               self.pos[1] - self.OImagerect[3] / 2 - self.OImagerect[3] / 8 + settings.CameraPos[1],
                                               math.floor(self.OImagerect[2] * self.HP / self.MaxHP),
                                               self.OImagerect[3] / 8))

        self.win.blit(self.image, (self.imagerect[0] + settings.CameraPos[0], self.imagerect[1] + settings.CameraPos[1], self.imagerect[2], self.imagerect[3]))
