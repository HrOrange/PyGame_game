import math
import pygame as game
from pygame.math import Vector2
import time
import playerClass
import zombieClass

class Opstacle:
    def __init__(self, pos, block, cam):
        self.pos = pos
        self.block = block
        self.cam = cam
        self.win = game.display.get_surface()
        self.OriginalImage = game.transform.scale(game.image.load("Images/WoodenBox.png"), (60, 60))
        self.imagerect = self.OriginalImage.get_rect()
        self.imagerect.center = (self.pos[0], self.pos[1])

    def CheckCol(self):
        pass
    def update(self):
        pass

    def DrawMe(self):
        DrawRect(self.win, self.pos, self.imagerect, (255, 0, 0))
        game.draw.circle(self.win, (0, 0, 255), self.pos, 10)
        game.draw.circle(self.win, (255, 0, 0), [int(self.pos[0] - self.imagerect[2] / 2), int(self.pos[1])], 10)

    def draw(self):
        self.win.blit(self.OriginalImage, self.imagerect)
        game.draw.circle(self.win, (255, 0, 255), [int(self.pos[0] + self.imagerect[2] / 2), int(self.pos[1] + self.imagerect[3] / 2)], 15)



class Button:
    def __init__(self, pos, size, text, color, func, font):
        self.pos = pos
        self.size = size
        self.win = game.display.get_surface()
        self.text = text
        self.color = color
        self.func = func
        self.font = font

    def update(self):
        if(game.mouse.get_pos()[0] > self.pos[0] and
        game.mouse.get_pos()[0] < self.pos[0] + self.size[0] and
        game.mouse.get_pos()[1] > self.pos[1] and
        game.mouse.get_pos()[1] < self.pos[1] + self.size[1]):
            #self.func(self)        hvis du vil kalde en funktion i classen
            self.func()

    def draw(self):
        reverseColor = (255 - self.color[0],  255 - self.color[1], 255 - self.color[2])
        game.draw.rect( self.win,
                        reverseColor,
                        (self.pos[0] - self.size[0] / 20,
                        self.pos[1] - self.size[1] / 20,
                        self.size[0] + self.size[0] / 10,
                        self.size[1] + self.size[1] / 10))
        game.draw.rect( self.win,
                        self.color,
                        (self.pos[0], self.pos[1],
                        self.size[0], self.size[1]))
        text = self.font.render(self.text, True, reverseColor)
        self.win.blit(text, (self.pos[0] + self.size[0] / 4,
                             self.pos[1] + self.size[1] / 4,
                             text.get_rect()[2], text.get_rect()[3]))
        """disse værdier der bruges til positionen på teksten er midlertidige,
        indtil jeg finder de rigtige værdier for størrelsen på fonten"""

        #hvis du vil kalde en funktion i classen
        """def Play(self):
            print("Play")"""
class TEXT:
    def __init__(self, win, pos, text, font, col):
        self.win = win
        self.pos = pos
        self.text = text
        self.font = font
        self.col = col
    def update(self):
        pass
    def DrawMe(self):
        pass
    def draw(self):
        text = self.font.render(self.text, True, self.col)
        rect = text.get_rect(center = self.pos)
        self.win.blit(text, rect)


def Play():
    print("Play")

def DrawRect(win, pos, rect, col):
    game.draw.rect(win, col, (pos[0] - rect[2] / 2, pos[1] - rect[3] / 2,
                   rect[2], rect[3]))
def DrawRectAlreadyCentered(win, pos, rect, col):
    game.draw.rect(win, col, (int(pos[0]), int(pos[1]), rect[2], rect[3]))
def DrawCircle(win, pos, col):
    game.draw.circle(win, col, [int(pos[0]), int(pos[1])], 25)
