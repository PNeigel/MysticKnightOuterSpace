
import pygame as pg
import numpy as np
import settings as settings

class level(pg.sprite.DirtySprite):
    def __init__(self):
        super(level, self).__init__()#
        self.whole = pg.image.load('../Gameart/Level/level_1.png')
        #self.whole = pg.transform.scale(self.whole, (int(3*settings.Width), int(3*settings.Height)))
        self.image = pg.Surface((settings.Width, settings.Height))
        self.srcrect = pg.Rect(0,0,settings.Width, settings.Height)
        self.image.blit(self.whole, (0,0), self.srcrect)
        self.image = pg.transform.scale(self.image, (settings.Width, settings.Height))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.path = [(1435,1085),(1435,-605),(2425,-605),(2425, 1010),(2980,1010)]
        #self.rect = pg.Rect(0,0,settings.Width, settings.Height)
        
    def update(self, cam_x, cam_y):
        
        self.srcrect.x = cam_x
        self.srcrect.y = cam_y
        self.image.fill(settings.black)
        self.image.blit(self.whole, (0,0), self.srcrect)
        #self.image = pg.transform.scale(self.image, (settings.Width, settings.Height))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        
        
