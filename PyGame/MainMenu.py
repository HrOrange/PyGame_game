import pygame as game
import sys
import time
from Classes import *
import random

#general
screenSize = [400, 400]
game.init()
game.mouse.set_cursor(*game.cursors.tri_left)
win = game.display.set_mode((screenSize[0], screenSize[1]))
game.display.set_caption("MainMenu")
font = game.font.Font(None, 40)



#holder for all my objects in the game/window
instances = []
instances.append(Button([100, 100], [100, 100], "play", (255, 255, 255), Play, font))

run = True
while run:
    game.time.delay(30)

    #print(game.event.get())
    for event in game.event.get():
        #general
        if(event.type == game.QUIT):
            run = False

    win.fill((255, 255, 255))
    pressed = game.key.get_pressed()
    #tegn objekter
    for i in instances:
        try:
            i.update()
        except:
            try:
                i.update(instances)
            except:
                i.update(pressed)
        i.draw()


    game.display.update()

game.quit()
#sys.exit()
