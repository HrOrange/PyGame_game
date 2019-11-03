import pygame as game
import time
import settings

class FPSCount:
    def __init__(self):
        self.c = time.time()
        self.currentFPS = 0

    def update(self):
        pass
    def draw(self):
        #FPS
        self.currentFPS += 1
        if(time.time() - self.c > 1):
            settings.FPS = self.currentFPS
            self.c = time.time()
            self.currentFPS = 0
        FPSText = settings.font.render(str(settings.FPS), True, (0, 0, 0))
        FPSTextRect = FPSText.get_rect()
        settings.win.blit(FPSText, (0, 0, FPSTextRect[2], FPSTextRect[3]))
