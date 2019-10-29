import pygame as game
import sys
import time
from Classes import *
from zombieClass import *
from playerClass import *
from bulletClass import *
import random

#general
game.init()
game.mouse.set_cursor(*game.cursors.broken_x)
screenSize = [450, 450]
win = game.display.set_mode((screenSize[0], screenSize[1]))
game.display.set_caption("Dummy Zombie")
font = game.font.Font(None, 50)
font.set_bold(True)

worldSize = [10000, 10000]
instances = []
CameraPos = [0, 0]
TimeBetweenZombieSpawn = 5
t = time.time()
run = True
move = True
player = Player(2, [100, 100], instances, CameraPos, font)
instances.append(player)
for x in range(2):
    instances.insert(0, Opstacle([random.randint(0, screenSize[0]),
                              random.randint(0, screenSize[0])], True, CameraPos))
#instances.insert(0, Zombie([300, 400], 3, instances, CameraPos))

#instances.insert(0, TEXT(win, [screenSize[0] - font.get_sizes[0], screenSize[1] - font.get_sizes[1]], "hejsa", font, size, (100, 0, 0)))

while run:
    game.time.delay(30)

    #spawn zombies
    """if(time.time() - t > TimeBetweenZombieSpawn):
        if(TimeBetweenZombieSpawn > 1):
            TimeBetweenZombieSpawn -= .1
        instances.insert(0, Zombie([random.randint(-100, 100), random.randint(-100, 100)], 3, instances, CameraPos))
        t = time.time()"""

    #print(game.event.get())
    for event in game.event.get():
        #general
        if(event.type == game.QUIT):
            run = False
        elif(event.type == game.MOUSEBUTTONDOWN):
            offset = [47, 17]
            Image = game.image.load("Images/PeterPanV3.png")
            size = player.OriginalImage.get_size()
            #instances.append(Bullet(15, player, instances, CameraPos))
                    #i.mousePress(instances)

    win.fill((255, 255, 255))

    #tegn objekter
    for i in instances:
        if(move):
            i.update()
        i.DrawMe()
        i.draw()
    if(move):
        move = player.GameOverCheck()

    game.display.update()
game.quit()
#sys.exit()
