import numpy as np
import pygame as pg
import settings as settings
import pygame.locals as loc
import tools as tools

tower_width = 200
tower_height = 200

class tesla_coil(pg.sprite.DirtySprite):

    def __init__(self, spawn_x, spawn_y):
        super(tesla_coil, self).__init__()
        self.x_pos = spawn_x*1.
        self.y_pos = spawn_y*1.
        self.animation_frame = 0
        self.spritesheet = []

        self.spritesheet.append(pg.image.load('../Gameart/towers/teslacoil/teslacoil0.png').convert_alpha())
        self.spritesheet.append(pg.image.load('../Gameart/towers/teslacoil/teslacoil1.png').convert_alpha())
        
        self.image = self.spritesheet[0]

        #self.image = pg.Surface((tower_width, tower_height))
        #self.image.set_colorkey(settings.black)
        #self.image.blit(self.spritesheet[0], (0,0), (0, 0, tower_width, tower_height))

        #self.image = self.image.convert()
        self.rect = self.image.get_rect()

        self.collision_rect = pg.Rect(self.x_pos, self.y_pos, 100, 100)
        self.rect.x, self.rect.y = tools.ScreenFromIngame(self.x_pos, self.y_pos)
        
        self.attack_CD = 0
        
        self.attack_radius = 300
        
        self.attack_rect = pg.Rect(self.x_pos-self.attack_radius, self.y_pos-self.attack_radius, 2*self.attack_radius, 2*self.attack_radius)
        
        self.target = None 
        
        self.projectiles = pg.sprite.Group()
        
        self.type = 1
        
        self.teslahit_sound = pg.mixer.Sound('../Gameart/Sounds/Tower/Shoot/Teslahit.wav')

    def update(self):
        
        self.projectiles.update()
        
        for proj in self.projectiles:
            if proj.finished:
                self.projectiles.remove(proj)
                self.teslahit_sound.play()
        
        self.attack_CD -= 1

        if self.animation_frame == 0:
            #self.image.fill(settings.black)
            #self.image.blit(self.spritesheet[0], (0,0), (0, 0, tower_width, tower_height))
            self.image = self.spritesheet[0]

        if self.animation_frame == 15:
            #self.image.fill(settings.black)
            #self.image.blit(self.spritesheet[1], (0,0), (0, 0, tower_width, tower_height))
            self.image = self.spritesheet[1]

        # Reset anim
        if self.animation_frame == 30:
            self.animation_frame = 0
        else:
            self.animation_frame +=1
            
        if self.attack_CD == -1:
            self.attack_CD = 90
