import math
import pygame as game
from pygame.math import Vector2
import time
from zombieClass import *
import Classes
from bulletClass import *

class Player:
    def __init__(self, vel, pos, instances, cam, font):
        self.vel = vel
        self.pos = pos
        self.cam = cam
        self.font = font
        self.instances = instances
        self.win = game.display.get_surface()
        self.OriginalImage = game.image.load("Images/ar-guyV3.png")
        self.imagerect = self.OriginalImage.get_rect()
        self.image = game.Surface((self.imagerect[2], self.imagerect[3]),
                                    game.SRCALPHA)
        self.dirAngle = 0
        self.bulletSpawn = Vector2(pos[0] + self.imagerect[2] + 47,
                                   pos[1] + self.imagerect[3] - 12)
        self.HitBoxSize = 25
        self.OHitBoxOffset = Vector2(-15, 0)
        self.HitBoxOffset = Vector2.rotate(self.OHitBoxOffset, self.dirAngle)

        self.HitTargets = [Classes.Opstacle]
        self.DeathBy = [zombieClass.Zombie]
        self.r = None
        self.TimeToReload = 3
        self.t = time.time()
        self.FireRate = 0.3

        #playerSettings
        self.MaxAmmo = 180
        self.magSize = 30
        self.ammo = self.magSize
        self.lives = 3
        self.heartImage = game.transform.scale(game.image.load("Images/Heart.png"), (40, 40))
        self.heartImageRect = self.heartImage.get_rect()
        #self.heartImageRect.center = [self.heartImageRect[2] / 2, self.heartImageRect[3] / 2]

    def update(self):
        pressed = game.key.get_pressed()
        if(pressed[game.K_s] or pressed[game.K_DOWN]):
            temp = [self.pos[0], self.pos[1] + self.vel]
            #if(self.CheckCol(temp)):
                #self.cam[1] += self.vel
            self.pos = temp
        if(pressed[game.K_w] or pressed[game.K_UP]):
            temp = [self.pos[0], self.pos[1] - self.vel]
            #if(self.CheckCol(temp)):
                #self.cam[1] -= self.vel
            self.pos = temp
        if(pressed[game.K_d] or pressed[game.K_RIGHT]):
            temp = [self.pos[0] + self.vel, self.pos[1]]
            #if(self.CheckCol(temp)):
                #self.cam[0] += self.vel
            self.pos = temp
        if(pressed[game.K_a] or pressed[game.K_LEFT]):
            temp = [self.pos[0] - self.vel, self.pos[1]]
            #if(self.CheckCol(temp)):
                #self.cam[0] -= self.vel
            self.pos = temp
        if(pressed[game.K_r]): #reload
            if(self.ammo != self.MaxAmmo and self.MaxAmmo > 0 and self.r is None):
                self.r = time.time()
        if(game.mouse.get_pressed()[0] == 1 and time.time() - self.t > self.FireRate and self.ammo > 0 and self.r is None): #full auto shoot
            self.instances.insert(0, Flash(self.win, self.instances, .08, self.cam))
            self.instances.insert(0, Bullet(15, self, self.instances, self.cam))
            self.t = time.time()
            self.ammo -= 1

        #reload
        if(self.r is not None):
            if(time.time() - self.r > self.TimeToReload):
                self.r = None
                if(self.MaxAmmo >= self.magSize - self.ammo):
                    self.MaxAmmo -= self.magSize - self.ammo
                    self.ammo = self.magSize
                else:
                    self.ammo = self.MaxAmmo
                    self.MaxAmmo = 0

        #updating the position where the bullets and flash spawn
        self.bulletSpawn = Vector2(47, 12)
        self.bulletSpawn = Vector2.rotate(self.bulletSpawn, self.dirAngle)
        self.bulletSpawn = Vector2(self.bulletSpawn[0] + self.pos[0],
                                   self.bulletSpawn[1] + self.pos[1])

        #updating the direction the person is looking at
        dir = [game.mouse.get_pos()[0] - self.pos[0],
               game.mouse.get_pos()[1] - self.pos[1]]
        tempAngle = self.dirAngle
        self.dirAngle = math.degrees(math.atan2(dir[1], dir[0]))
        self.image = game.transform.rotate(self.OriginalImage, -self.dirAngle)
        self.imagerect = self.image.get_rect(center = (self.pos[0], self.pos[1]))

        #updating for collision and updating hitboxoffset
        self.HitBoxOffset = Vector2.rotate(self.OHitBoxOffset, self.dirAngle)
        if(tempAngle != self.dirAngle):
            self.pos = self.CheckCol2()

    def CheckCol(self, tempPos):
        move = True

        cand = self.instances[0]
        for i in self.instances:
            if(type(i) == Classes.Opstacle):
                if(math.sqrt(abs(i.pos[0] - tempPos[0])**2 + abs(i.pos[1] - tempPos[1])**2) < math.sqrt(abs(cand.pos[0] - tempPos[0])**2 + abs(cand.pos[1] - tempPos[1])**2)):
                    cand = i
        #if(math.sqrt(abs(cand.pos[0] - tempPos[0])**2 + abs(cand.pos[1] - tempPos[1])**2) < math.sqrt((self.imagerect[2] - tempPos[0])**2 + (self.imagerect[3] - tempPos[1])**2)):
        if(abs(cand.pos[0] - self.pos[0]) < self.HitBoxSize and abs(cand.pos[1] - self.pos[1]) < self.HitBoxSize):
            if(tempPos[1] + self.HitBoxSize + self.HitBoxOffset[1] > cand.pos[1] - cand.imagerect[3] / 2 and #top
               tempPos[1] - self.HitBoxSize + self.HitBoxOffset[1] < cand.pos[1] + cand.imagerect[3] / 2 and #down
               tempPos[0] + self.HitBoxSize + self.HitBoxOffset[0] > cand.pos[0] - cand.imagerect[2] / 2 and #left
               tempPos[0] - self.HitBoxSize + self.HitBoxOffset[0] < cand.pos[0] + cand.imagerect[2] / 2): #right
                move = False
        return move
    def CheckCol2(self):
        temp = self.pos

        cand = self.instances[0]
        for i in self.instances:
            if(type(i) in self.HitTargets):
                if(abs(i.pos[0] - temp[0]) + abs(i.pos[1] - temp[1]) < abs(cand.pos[0] - temp[0]) + abs(cand.pos[1] - temp[1])):
                    cand = i
        if(abs(cand.pos[1] - temp[1]) - self.HitBoxSize - cand.imagerect[3] / 2 < 0 and
           abs(cand.pos[0] - temp[0]) - self.HitBoxSize - cand.imagerect[2] / 2 < 0):
        #if(abs(cand.pos[0] - temp[0]) < self.HitBoxSize and abs(cand.pos[1] - temp[1]) < self.HitBoxSize):
            print("Inside")
            difX = temp[0] - i.pos[0]
            difY = temp[1] - i.pos[1]
            if(abs(difX) > abs(difY)):
                if(difX > 0):
                    print("right")
                    temp[0] += (i.pos[0] + i.imagerect[2] / 2) - (temp[0] - self.HitBoxSize - self.HitBoxOffset[0])
                else:
                    print("left")
                    temp[0] -= (i.pos[0] - i.imagerect[2] / 2) - (temp[0] + self.HitBoxSize + self.HitBoxOffset[0])
            elif(difY > 0):
                print("down")
                temp[1] += (i.pos[1] - i.imagerect[3] / 2) - (temp[1] + self.HitBoxSize + self.HitBoxOffset[1])
            else:
                print("Up")
                temp[1] -= temp[1] + self.HitBoxSize + self.HitBoxOffset[1] - i.pos[1] - i.imagerect[3] / 2
        return temp
        #if(temp[1] + self.HitBoxSize + self.HitBoxOffset[1] > i.pos[1] - i.imagerect[3] / 2 and
         #  temp[1] - self.HitBoxSize + self.HitBoxOffset[1] < i.pos[1] + i.imagerect[3] / 2 and
          # temp[0] + self.HitBoxSize + self.HitBoxOffset[0] > i.pos[0] - i.imagerect[2] / 2 and
           #temp[0] - self.HitBoxSize + self.HitBoxOffset[0] < i.pos[0] + i.imagerect[2] / 2):"""

    def GameOverCheck(self):
        IAmAlive = True
        for i in self.instances:
            if(type(i) in self.DeathBy):
                if(self.pos[1] + self.HitBoxSize + self.HitBoxOffset[1] > i.pos[1] - i.imagerect[3] / 2 and #top
                   self.pos[1] - self.HitBoxSize + self.HitBoxOffset[1] < i.pos[1] + i.imagerect[3] / 2 and #down
                   self.pos[0] + self.HitBoxSize + self.HitBoxOffset[0] > i.pos[0] - i.imagerect[2] / 2 and #left
                   self.pos[0] - self.HitBoxSize + self.HitBoxOffset[0] < i.pos[0] + i.imagerect[2] / 2):
                    self.lives -= 1
                    self.instances.remove(i)
                    if(self.lives == 0):
                        print("GAMEOVER")
                        IAmAlive = False
        return IAmAlive

    def draw(self):
        imagerect = self.imagerect
        #imagerect[0] += self.cam[0]
        #imagerect[1] += self.cam[1]
        self.win.blit(self.image, imagerect)

        #UI
        for x in range(self.lives):
            self.win.blit(self.heartImage, (x * self.heartImageRect[2] + x * self.heartImageRect[2] / 10, 0, self.heartImageRect[2], self.heartImageRect[3]))
        ammoText = self.font.render(str(self.ammo), True, (0, 0, 0))
        MaxAmmoText = self.font.render(str(self.MaxAmmo), True, (0, 0, 0))
        HashText = self.font.render("/", True, (0, 0, 0))
        ammoRect = ammoText.get_rect()
        MaxAmmoRect = MaxAmmoText.get_rect()
        HashRect = HashText.get_rect()
        #da HashText kun indeholder 1. bogstav, er det naturligt at den ville være den centrale unit for texts bredde pr. bogstav
        self.win.blit(ammoText, (game.display.Info().current_w - (len(str(self.ammo)) + len(str(self.MaxAmmo)) + 2) * 23, game.display.Info().current_h - ammoRect[3], ammoRect[2], ammoRect[3]))
        self.win.blit(HashText, (game.display.Info().current_w - (len(str(self.MaxAmmo)) + 1.3) * 23, game.display.Info().current_h - HashRect[3], HashRect[2], HashRect[3]))
        self.win.blit(MaxAmmoText, (game.display.Info().current_w - len(str(self.MaxAmmo)) * 23, game.display.Info().current_h - MaxAmmoRect[3], MaxAmmoRect[2], MaxAmmoRect[3]))

    def DrawMe(self):
        game.draw.circle(self.win, (0, 255, 100), [int(self.pos[0] + self.HitBoxSize + self.HitBoxOffset[0]), int(self.pos[1] + self.HitBoxOffset[1])], 8)
        game.draw.circle(self.win, (255, 255, 100), [int(self.pos[0] + self.HitBoxOffset[0]), int(self.pos[1] + self.HitBoxOffset[1])], int(self.HitBoxSize))
