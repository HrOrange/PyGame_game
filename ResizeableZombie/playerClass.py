import math
import pygame as game
from pygame.math import Vector2
import time
import zombieClass
import Classes
import bulletClass
import opstacleClass
import settings
class Player:
    def __init__(self, vel, pos):
        self.vel = vel
        self.pos = pos

        self.win = game.display.get_surface()
        self.OriginalImage = game.image.load("Images/ar-guyV3.png").convert_alpha()
        self.imagerect = self.OriginalImage.get_rect()
        self.image = game.Surface((self.imagerect[2], self.imagerect[3]),
                                    game.SRCALPHA)
        self.mask = game.mask.from_surface(self.image)

        self.dirAngle = 0
        self.bulletSpawn = Vector2(pos[0] + self.imagerect[2] + 47,
                                   pos[1] + self.imagerect[3] - 12)
        self.HitBoxSize = 25
        self.OHitBoxOffset = Vector2(-15, 0)
        self.HitBoxOffset = Vector2.rotate(self.OHitBoxOffset, self.dirAngle)

        self.HitTargets = [opstacleClass.Opstacle]
        self.HurtBy = [zombieClass.Zombie]
        self.r = None
        self.TimeToReload = 2.0
        self.t = time.time()
        self.FireRate = 0.15

        #playerSettings
        self.MaxAmmo = settings.maxAmmo
        self.magSize = 30
        self.ammo = self.magSize
        self.lives = 5
        self.heartImage = game.transform.scale(game.image.load("Images/Heart.png"), (40, 40))
        self.heartImageRect = self.heartImage.get_rect()
        self.opos = self.pos
        self.ShottingSound = game.mixer.Sound("Audio/Gunshot.wav")
        #self.ReloadSound = game.mixer.Sound("Audio/Reload.wav")

    def update(self):
        pressed = game.key.get_pressed()
        if(pressed[game.K_s] or pressed[game.K_DOWN]):
            temp = [self.pos[0], self.pos[1] + self.vel]
            if(self.CheckCol(temp)):
                self.pos = temp
        if(pressed[game.K_w] or pressed[game.K_UP]):
            temp = [self.pos[0], self.pos[1] - self.vel]
            if(self.CheckCol(temp)):
                self.pos = temp
        if(pressed[game.K_d] or pressed[game.K_RIGHT]):
            temp = [self.pos[0] + self.vel, self.pos[1]]
            if(self.CheckCol(temp)):
                self.pos = temp
        if(pressed[game.K_a] or pressed[game.K_LEFT]):
            temp = [self.pos[0] - self.vel, self.pos[1]]
            if(self.CheckCol(temp)):
                self.pos = temp
        settings.CameraPos = [-(self.pos[0] - self.opos[0]), -(self.pos[1] - self.opos[1])]

        if(pressed[game.K_r]): #reload
            if(self.ammo != self.MaxAmmo and self.MaxAmmo > 0 and self.r is None):
                self.r = time.time()
                #self.ReloadSound.play()
        if(game.mouse.get_pressed()[0] == 1 and time.time() - self.t > self.FireRate and self.ammo > 0 and self.r is None): #full auto shoot
            settings.instances.insert(0, bulletClass.Flash(self.win, .08))
            settings.instances.insert(0, bulletClass.Bullet(15))
            self.ShottingSound.play()
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

        #updating the direction the person is looking at
        dir = [game.mouse.get_pos()[0] - self.opos[0],
               game.mouse.get_pos()[1] - self.opos[1]]
        tempAngle = self.dirAngle
        self.dirAngle = math.degrees(math.atan2(dir[1], dir[0]))
        self.image = game.transform.rotate(self.OriginalImage, -self.dirAngle)
        self.imagerect = self.image.get_rect(center = self.pos)
        self.mask = game.mask.from_surface(self.image)

        #updating the position where the bullets and flash spawn
        self.bulletSpawn = Vector2(47, 12)
        self.bulletSpawn = Vector2.rotate(self.bulletSpawn, self.dirAngle)
        self.bulletSpawn = Vector2(self.bulletSpawn[0] + self.pos[0],
                                   self.bulletSpawn[1] + self.pos[1])

        #updating for collision and updating hitboxoffset
        self.HitBoxOffset = Vector2.rotate(self.OHitBoxOffset, self.dirAngle)
        if(tempAngle != self.dirAngle):
            self.pos = self.CheckCol2()

        self.CheckCol3()

        #CheckCol()  sører for at du ikke kan gå ind i en box
        #CheckCol2() checker om du er inde i en box, hvorefter den skuber dig ud hvis du er i den (brugt fordi du kan rotere ind i en box)
        #CheckCol3() checker om enemies er i dig
        #CheckCol4() checker for hvorvidt playerens pixels er i kontakt med nogen andens


    def CheckCol(self, tempPos):
        move = True
        if(len(settings.instances) == 2):
            return move

        cand = None
        for i in settings.instances:
            if(type(i) in self.HitTargets):
                cand = i
                break
        if(type(cand) == None):
            return move

        for i in settings.instances:
            if(type(i) in self.HitTargets):
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
        if(len(settings.instances) == 1):
            return self.pos
        else:
            temp = self.pos

        cand = settings.instances[0]
        for i in settings.instances:
            if(type(i) in self.HitTargets and i != self):
                if(abs(i.pos[0] - temp[0]) + abs(i.pos[1] - temp[1]) < abs(cand.pos[0] - temp[0]) + abs(cand.pos[1] - temp[1])):
                    cand = i
        #if(difYY < 0 and difXX < 0):
        try:
            if(cand.pos[0] - cand.imagerect[2] / 2 < temp[0] + self.HitBoxOffset[0] + self.HitBoxSize and #left side
               cand.pos[0] + cand.imagerect[2] / 2 > temp[0] + self.HitBoxOffset[0] - self.HitBoxSize and #right side
               cand.pos[1] - cand.imagerect[3] / 2 < temp[1] + self.HitBoxOffset[1] + self.HitBoxSize and #up side
               cand.pos[1] + cand.imagerect[3] / 2 > temp[1] + self.HitBoxOffset[1] - self.HitBoxSize): #down side
                difX = temp[0] + self.HitBoxOffset[0] - cand.pos[0]
                difY = temp[1] + self.HitBoxOffset[1] - cand.pos[1]
                #print(difX)
                #print(difY)

                if(abs(difX) > abs(difY)):
                    if(difX > 0):
                        temp[0] += abs((temp[0] + self.HitBoxOffset[0] - self.HitBoxSize) - (cand.pos[0] + cand.imagerect[2] / 2))
                    else:
                        temp[0] -= (temp[0] + self.HitBoxOffset[0] + self.HitBoxSize) - (cand.pos[0] - cand.imagerect[2] / 2)
                elif(difY > 0):
                    temp[1] += abs((temp[1] + self.HitBoxOffset[1] - self.HitBoxSize) - (cand.pos[1] + cand.imagerect[3] / 2))
                else:
                    temp[1] -= abs((temp[1] + self.HitBoxOffset[1] + self.HitBoxSize) - (cand.pos[1] - cand.imagerect[3] / 2))
        except:
            pass

        return temp
    def CheckCol3(self):
        if(len(settings.instances) == 1):
            return self.pos
        else:
            temp = self.pos

        cand = None
        for i in settings.instances:
            if(type(i) in self.HurtBy):
                cand = i
                break
        if(type(cand) == None):
            return self.pos

        for i in settings.instances:
            if(type(i) in self.HurtBy and i != self):
                if(abs(i.pos[0] - temp[0]) + abs(i.pos[1] - temp[1]) < abs(cand.pos[0] - temp[0]) + abs(cand.pos[1] - temp[1])):
                    cand = i
        try:
            res = self.mask.overlap(cand.mask, [int((cand.pos[0] - cand.imagerect[2] / 2) - (self.pos[0] - self.imagerect[2] / 2)),
                                             int((cand.pos[1] - cand.imagerect[3] / 2) - (self.pos[1] - self.imagerect[3] / 2))])
            if(res != None):
                self.lives -= 1
                settings.deleteMe.append(cand)
                if(self.lives <= 0):
                    settings.InGame = False
                    for x in settings.instances:
                        settings.instances.remove(x)
                    #make MainMenu
                    playButtonText = "Play"
                    playButton = Classes.PlayButton([settings.screenSize[0] / 2 - len(playButtonText) * settings.fontSize[0], settings.screenSize[1] / 2 - settings.fontSize[1]],[200, 40], playButtonText, (200, 200, 200))
                    settings.instances.insert(0, playButton)
        except:
            pass
    def CheckCol4(self):
        for i in settings.instances:
            try:
                res = self.mask.overlap(i.mask, [int((i.pos[0] - i.imagerect[2] / 2) - (self.pos[0] - self.imagerect[2] / 2)), int((i.pos[1] - i.imagerect[3] / 2) - (self.pos[1] - self.imagerect[3] / 2))])
                if(res != None):
                    print(res)
            except:
                pass

    def draw(self):
        self.win.blit(self.image, (self.imagerect[0] + settings.CameraPos[0], self.imagerect[1] + settings.CameraPos[1], self.imagerect[2], self.imagerect[3]))
    def DrawMe(self):
        game.draw.rect(self.win, (255, 0, 0), (self.imagerect[0] + settings.CameraPos[0], self.imagerect[1] + settings.CameraPos[1], self.imagerect[2], self.imagerect[3]))
        game.draw.circle(self.win, (0, 255, 100), [int(self.pos[0] + self.HitBoxSize + self.HitBoxOffset[0] + settings.CameraPos[0]), int(self.pos[1] + self.HitBoxOffset[1] + settings.CameraPos[1])], 8)
        game.draw.circle(self.win, (255, 255, 100), [int(self.pos[0] + self.HitBoxOffset[0] + settings.CameraPos[0]), int(self.pos[1] + self.HitBoxOffset[1] + settings.CameraPos[1])], int(self.HitBoxSize))
