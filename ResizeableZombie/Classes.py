import pygame as game
from pygame.math import Vector2
import time
import random
import math
import playerClass
import zombieClass
import opstacleClass
import HUDClass
import settings
import FPSCountClass

class PlayButton:
    def __init__(self, pos, size, text, col):
        self.pos = pos
        self.size = size
        self.win = game.display.get_surface()
        self.col = col

        self.rect = game.Surface((size[0], size[1]))
        self.rect = self.rect.get_rect(center = self.pos)
        self.text = settings.font.render(text, True, (255 - col[0], 255 - col[1], 255 - col[2]))
        self.textRect = self.text.get_rect(center = self.pos)

    def update(self):
        if(game.mouse.get_pressed()[0] == 1 and
           game.mouse.get_pos()[0] > self.pos[0] - self.size[0] / 2 and
           game.mouse.get_pos()[0] < self.pos[0] + self.size[0] / 2 and
           game.mouse.get_pos()[1] > self.pos[1] - self.size[1] / 2 and
           game.mouse.get_pos()[1] < self.pos[1] + self.size[1] / 2):
            self.Play()         #hvis du vil kalde en funktion i classen
            #self.func              #hvis du vil kalde en funktion uden for klassen

    def draw(self):
        game.draw.rect( self.win,
                        self.col,
                        self.rect)
        self.win.blit(self.text, self.textRect)
        """disse værdier der bruges til positionen på teksten er midlertidige,
        indtil jeg finder de rigtige værdier for størrelsen på fonten"""

    #hvis du vil kalde en funktion i classen
    def Play(self):
        while(len(settings.instances) > 1):
            for i in settings.instances:
                if(type(i) != FPSCountClass.FPSCount):
                    settings.instances.remove(i)

        settings.InGame = True
        game.mixer.music.load("Audio/InGameSoundtrack.mp3")
        game.mixer.music.play(-1)
        settings.instances.insert(0, HUDClass.HUD())
        settings.player = playerClass.Player(3, [settings.screenSize[0] / 2, settings.screenSize[1] / 2])
        settings.instances.append(settings.player)
        settings.score = 0
        #settings.instances.insert(0, zombieClass.Zombie([300, 400], 3))
        for x in range(1):
            settings.instances.insert(0, opstacleClass.Opstacle([random.randint(0, 300), random.randint(0, 300)], True))

class TEXT:
    def __init__(self, pos, text, col):
        self.pos = pos
        self.text = text
        self.col = col
    def update(self):
        pass
    def DrawMe(self):
        pass
    def draw(self):
        text = settings.font.render(self.text, True, self.col)
        rect = text.get_rect(center = self.pos)
        settings.win.blit(text, rect)


class FPSButton:
    def __init__(self, pos, size, col, f):
        self.extraHardness = 5
        self.f = f
        self.pos = pos
        self.size = size
        self.col = col
        self.win = game.display.get_surface()

        self.rect = game.Surface((size[0], size[1]))
        self.rect = self.rect.get_rect(center = self.pos)
        self.text = settings.font.render(str(f), True, (255 - col[0], 255 - col[1], 255 - col[2]))
        self.textRect = self.text.get_rect(center = self.pos)

    def update(self):
        if(game.mouse.get_pressed()[0] == 1 and
           game.mouse.get_pos()[0] > self.pos[0] - self.size[0] / 2 and
           game.mouse.get_pos()[0] < self.pos[0] + self.size[0] / 2 and
           game.mouse.get_pos()[1] > self.pos[1] - self.size[1] / 2 and
           game.mouse.get_pos()[1] < self.pos[1] + self.size[1] / 2):
            if(settings.FPSCap != self.f * 100):
                print(self.f)
                settings.FPSCap = self.f * 100
                settings.adjustedFPS = 30 - (self.f * 100) / 200 * 15 + self.extraHardness
                print(settings.adjustedFPS)
                #delay(30) = 30
                #delay(0) = 800

    def draw(self):
        game.draw.rect( self.win,
                        self.col,
                        self.rect)
        self.win.blit(self.text, self.textRect)






def DrawRect(win, pos, rect, col):
    game.draw.rect(win, col, (pos[0] - rect[2] / 2, pos[1] - rect[3] / 2,
                   rect[2], rect[3]))
def DrawRectAlreadyCentered(win, pos, rect, col):
    game.draw.rect(win, col, (int(pos[0]), int(pos[1]), rect[2], rect[3]))
def DrawCircle(win, pos, col):
    game.draw.circle(win, col, [int(pos[0]), int(pos[1])], 25)
