import numpy as np
import pygame as pg
import settings as settings
import pygame.locals as loc
import tools as tools

tower_width = 200
tower_height = 200

class rail_gun(pg.sprite.DirtySprite):

    def __init__(self, spawn_x, spawn_y):
        super(rail_gun, self).__init__()
        self.x_pos = spawn_x*1.
        self.y_pos = spawn_y*1.
        self.animation_frame = 0
        self.spritesheet = []

        self.spritesheet.append(pg.image.load('../Gameart/towers/railgun/railgun0.png').convert_alpha())
        self.spritesheet.append(pg.image.load('../Gameart/towers/railgun/railgun1.png').convert_alpha())
        self.spritesheet.append(pg.image.load('../Gameart/towers/railgun/railgun2.png').convert_alpha())
        
        self.image = self.spritesheet[0]

        #self.image = pg.Surface((tower_width, tower_height))
        #self.image.set_colorkey(settings.black)
        #self.image.blit(self.spritesheet[0], (0,0), (0, 0, tower_width, tower_height))

        #self.image = self.image.convert()
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = tools.ScreenFromIngame(self.x_pos, self.y_pos)

        self.collision_rect = pg.Rect(self.x_pos, self.y_pos, 100, 100)
        
        self.attack_CD = 0
        
        self.attack_radius = 100
        
        self.attack_rect = pg.Rect(self.x_pos-self.attack_radius, self.y_pos-self.attack_radius, 2*self.attack_radius, 2*self.attack_radius)
        
        self.target = None 
        
        self.type = 0

    def update(self):
        
        self.attack_CD -= 1

        if self.animation_frame == 0:
            #self.image.fill(settings.black)
            #self.image.blit(self.spritesheet[1], (0, 0), (0, 0, tower_width, tower_height))
            self.image = self.spritesheet[0]

        if self.animation_frame == 15:
            #self.image.fill(settings.black)
            #self.image.blit(self.spritesheet[0], (0,0), (0, 0, tower_width, tower_height))
            self.image = self.spritesheet[1]

        if self.animation_frame == 30:
            #self.image.fill(settings.black)
            #self.image.blit(self.spritesheet[2], (0,0), (0, 0, tower_width, tower_height))
            self.image = self.spritesheet[2]

        if self.animation_frame == 45:
            #self.image.fill(settings.black)
            #self.image.blit(self.spritesheet[0], (0,0), (0, 0, tower_width, tower_height))
            self.image = self.spritesheet[0]

        # Reset anim
        if self.animation_frame == 60:
            self.animation_frame = 0
        else:
            self.animation_frame += 1
        
        if self.attack_CD == -1:
            self.attack_CD = 30
