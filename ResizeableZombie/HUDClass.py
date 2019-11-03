import pygame as game
import settings
import time

class HUD:
    def update(self):
        pass
    def draw(self):
        settings.font = game.font.Font(None, 50)
        for x in range(settings.player.lives):
            #print(x * settings.player.heartImageRect[2] + x * settings.player.heartImageRect[2] / 10 + settings.screenSize[0] / 2)
            settings.player.win.blit(settings.player.heartImage, (x * settings.player.heartImageRect[2] + x * settings.player.heartImageRect[2] / 10, settings.screenSize[1] - settings.player.heartImageRect[3], settings.player.heartImageRect[2], settings.player.heartImageRect[3]))
        #time.sleep(10)
        KillText = settings.font.render(str(settings.score), True, (255, 0, 0))
        KillTextRect = KillText.get_rect()
        settings.player.win.blit(KillText, (settings.screenSize[0] - len(str(settings.score)) * 23, 0, KillTextRect[2], KillTextRect[3]))

        #ammo UI
        ammoInfoText = settings.font.render(str(settings.player.ammo) + " / " + str(settings.player.MaxAmmo), True, (0, 0, 0))
        ammoRect = ammoInfoText.get_rect()
        #da HashText kun indeholder 1. bogstav, er det naturligt at den ville være den centrale unit for texts bredde pr. bogstav
        settings.player.win.blit(ammoInfoText, (game.display.Info().current_w - len(str(settings.player.ammo) + " / " + str(settings.player.MaxAmmo)) * 16, game.display.Info().current_h - ammoRect[3], ammoRect[2], ammoRect[3]))
