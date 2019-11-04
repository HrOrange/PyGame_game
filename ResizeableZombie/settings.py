import pygame as game
import time
import random
import math

global instances
global player
global screenSize
global font, fontSize
global worldSize
global CameraPos
global TimeBetweenZombieSpawn
global move, run, InGame
global score
global deleteMe
global FPS
global win
global maxAmmo
global ZombieCount
global DeltaT
global ZombieSpeed
global ZombieSize
global bulletDamage

#general
game.mixer.init()
game.init()
game.mouse.set_cursor(*game.cursors.broken_x)
screenSize = [450, 450]
win = game.display.set_mode((screenSize[0], screenSize[1]))
game.display.set_caption("Sizeable Zombie")

#variables
instances = []
deleteMe = []
player = None
font = game.font.Font(None, 50)
fontSize = [font.render("", True, (0, 0, 0)).get_rect()[2], font.render("", True, (0, 0, 0)).get_rect()[3]]
font.set_bold(True)
worldSize = [10000, 10000]
CameraPos = [0, 0]
TimeBetweenZombieSpawn = 2
ZombieSize = 1
maxAmmo = 180
ZombieCount = 0
ZombieSpeed = 1.5
DeltaT = 0
bulletDamage = 30

#State of game
run = True
move = True
InGame = False
score = 0
FPS = 0

#OutsideGame
file = open("Highscore.txt", "r")
HighScore = float(file.readline()[0:len(file.readline()) - 1])
file.close()
