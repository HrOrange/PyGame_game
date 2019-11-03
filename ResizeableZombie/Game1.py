import pygame as game
import sys
import time
import random
from Classes import *
from zombieClass import *
from playerClass import *
from bulletClass import *
from FPSCountClass import *
import settings

#make MainMenu
game.mixer.music.load("Audio/MainMenuSoundtrack.mp3")
game.mixer.music.play(-1)
playButtonText = "Play"
playButton = PlayButton([settings.screenSize[0] / 2, settings.screenSize[1] / 2],[200, 40], playButtonText, (200, 200, 200))
settings.instances.insert(0, FPSCount())
settings.instances.insert(0, TEXT([settings.screenSize[0] / 2, settings.screenSize[1] * 0.7], "Difficulty", (55, 55, 55)))
for x in range(1, 5):
    settings.instances.insert(0, FPSButton([x / 5 * settings.screenSize[0], settings.screenSize[1] * 0.8], [settings.screenSize[0] / 5 - settings.screenSize[0] / 25, settings.screenSize[1] / 12], [200, 200, 200], x))
settings.instances.insert(0, playButton)

t = time.time()

while settings.run:
    #settings.DeltaT = game.time.Clock().tick() / 1000
    game.time.Clock().tick(60)

    #spawn zombies
    if(settings.InGame):
        if(settings.ZombieCount < 10):
            if(time.time() - t > settings.TimeBetweenZombieSpawn):
                if(settings.ZombieSize < 30):
                    settings.ZombieSize += 1
                r = random.randint(1, 4)
                try:
                    if(r == 1):
                        settings.instances.insert(0, Zombie([random.randint(int(settings.player.pos[0]) - 500, int(settings.player.pos[0]) - 200), random.randint(int(settings.player.pos[1]) - 500, int(settings.player.pos[0]) + 500)], 3))
                    elif(r == 2):
                        settings.instances.insert(0, Zombie([random.randint(int(settings.player.pos[0]) + 200, int(settings.player.pos[0]) + 500), random.randint(int(settings.player.pos[1]) - 500, int(settings.player.pos[0]) + 500)], 3))
                    elif(r == 3):
                        settings.instances.insert(0, Zombie([random.randint(int(settings.player.pos[0]) - 500, int(settings.player.pos[0]) + 500), random.randint(int(settings.player.pos[1]) - 500, int(settings.player.pos[0]) - 200)], 3))
                    elif(r == 4):
                        settings.instances.insert(0, Zombie([random.randint(int(settings.player.pos[0]) - 500, int(settings.player.pos[0]) + 500), random.randint(int(settings.player.pos[1]) + 200, int(settings.player.pos[0]) + 500)], 3))
                    t = time.time()
                    settings.ZombieCount += 1
                except:
                    pass

    for event in game.event.get():
        #general
        if(event.type == game.QUIT):
            settings.run = False

    settings.win.fill((255, 255, 255))

    #tegn objekter
    if(settings.InGame):
        for i in settings.instances:
            i.update()
            #i.DrawMe()
            i.draw()
        if(len(settings.deleteMe) > 0):
            for x in settings.deleteMe:
                try:
                    settings.deleteMe.remove(x)
                    settings.instances.remove(x)
                except:
                    pass
    else:
        for i in settings.instances:
            try:
                i.update()
            except:
                pass
            try:
                i.draw()
            except:
                pass

    game.display.update()

game.quit()
#sys.exit()
