import numpy as np
import pygame as pg
import settings as settings
import pygame.locals as loc
import tools as tools

projectile_width = 50
projectile_height = 50

class projectile(pg.sprite.DirtySprite):
    
    def __init__(self, x, y, target):
        super(projectile, self).__init__()
        self.x_pos = x
        self.y_pos = y
        self.animation_frame = 0
        self.image = pg.image.load('../Gameart/Lightning2.png').convert_alpha()
        #self.image = pg.transform.scale(self.image, (20,20))
        self.image = pg.transform.scale(self.image, (projectile_width, projectile_height))
        #self.image.set_colorkey(settings.black)
        #self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        self.collision_rect = pg.Rect(self.x_pos, self.y_pos, 100, 100)
        
        self.target = target
        
        self.finished = False
        
    def update(self):
        
        if not self.target is None:
            
            target_x, target_y = self.target.x_pos, self.target.y_pos
            dist_x = target_x - self.x_pos
            dist_y = target_y - self.y_pos
            self.direction = np.asarray([dist_x, dist_y])
            if np.linalg.norm(self.direction) < 30:
                if not self.finished:
                    self.target.hp -= 40
                self.finished = True
            if np.any(self.direction):
                self.direction /= np.linalg.norm(self.direction)
            self.x_pos += self.direction[0]*5
            self.y_pos += self.direction[1]*5
            
            self.collision_rect.x = self.x_pos - 10
            self.collision_rect.y = self.y_pos - 10
            
            self.rect.x, self.rect.y = tools.ScreenFromIngame(self.x_pos, self.y_pos)
            self.rect.x -= 50
            self.rect.y -= 50
        
        