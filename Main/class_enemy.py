import numpy as np
import pygame as pg
import settings as settings
import pygame.locals as loc
import tools as tools

enemy_width = 120
enemy_height = 120

class enemy(pg.sprite.DirtySprite):
    
    def __init__(self, spawn_x, spawn_y, typ):
        super(enemy, self).__init__()
        
        self.typ = typ
        
        if typ == 0:
            self.sprite_width = 150
            self.sprites_left = []
            self.sprites_right = []
            for i in range(3):
                self.sprites_left.append(pg.image.load('../Gameart/Enemies/Alien/Cart/AnimFlag/Left/%d.png' % i).convert_alpha())
                self.sprites_left[-1] = pg.transform.scale(self.sprites_left[-1], (4*150/7,150))
                self.sprites_right.append(pg.image.load('../Gameart/Enemies/Alien/Cart/AnimFlag/Right/%d.png' % i).convert_alpha())
                self.sprites_right[-1] = pg.transform.scale(self.sprites_right[-1], (4*150/7,150))
            self.collision_radius = 50
            
            self.max_HP = 400
            self.hp = 400
            
            self.path_dmg = 10
        
            self.speed = 1.2
            
            self.playerdmg = 10
            
        if typ == 1:
            self.sprite_width = 230
            self.sprites_left = []
            self.sprites_right = []
            for i in range(5):
                self.sprites_left.append(pg.image.load('../Gameart/Enemies/Alien/Boss/Walk/Left/%d.png' % i).convert_alpha())
                self.sprites_left[-1] = pg.transform.scale(self.sprites_left[-1], (230*2,150*2))
                self.sprites_right.append(pg.image.load('../Gameart/Enemies/Alien/Boss/Walk/Right/%d.png' % i).convert_alpha())
                self.sprites_right[-1] = pg.transform.scale(self.sprites_right[-1], (230*2,150*2))
            self.collision_radius = 100
            
            self.max_HP = 1300
            self.hp = 1300
            
            self.path_dmg = 20
        
            self.speed = 1
            
            self.playerdmg = 20
            
        self.x_pos = spawn_x*1.
        self.y_pos = spawn_y*1.
        self.animation_frame = 0
        self.image = self.sprites_right[0]
        #self.image = self.facing_right[0]
        #self.image = pg.Surface((enemy_width, enemy_height))
        #self.image.set_colorkey(settings.white)
        #self.image.blit(self.spritesheet, (0,0), (0, 0, 100, 100))
        #self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.path = [(1485,1085),(1485,-605),(2475,-605),(2475, 1010),(3200,1010)]
        self.path_position = 0
        self.collision_rect = pg.Rect(self.x_pos - self.collision_radius,
                                      self.y_pos - self.collision_radius,
                                      2*self.collision_radius,
                                      2*self.collision_radius)
        self.direction = np.asarray([1.,0.])
        
        self.destroy_flag = False
        self.remove_path_hp = False
        
    def update(self):
        
        self.animation_frame += 1
            
        # WALK ALONG PATH
        
        if self.hp <= 0:
            self.destroy_flag = True
        if self.path_position == len(self.path):
            self.destroy_flag = True
            self.remove_path_hp = True
        
        
        
        if self.path_position < len(self.path):
        
            target_x, target_y = self.path[self.path_position]
            dist_x = target_x - self.x_pos
            dist_y = target_y - self.y_pos
            self.direction = np.asarray([dist_x, dist_y])
            if np.any(self.direction):
                self.direction /= np.linalg.norm(self.direction)
            self.x_pos += self.direction[0]*self.speed
            self.y_pos += self.direction[1]*self.speed

            self.collision_rect.x = self.x_pos - self.collision_radius
            self.collision_rect.y = self.y_pos - self.collision_radius
            self.rect.x, self.rect.y = tools.ScreenFromIngame(self.x_pos, self.y_pos)
            #self.rect.x -= 50
            #self.rect.y -= 50
            
            if np.abs(dist_x) < 5 and np.abs(dist_y) < 5:
                
                self.path_position += 1
                
        if self.direction[0] >= self.direction[1]:
            FACING_RIGHT = True
            FACING_LEFT = False
        else:
            FACING_RIGHT = False
            FACING_LEFT = True
                
        if self.typ == 0:
        
            anim_speed = 8
            
            for i in range(3):
                
                if self.animation_frame == anim_speed * i:
                    if FACING_LEFT:
                        self.image = self.sprites_left[i]
                    elif FACING_RIGHT:
                        self.image = self.sprites_right[i]
                        
            if self.animation_frame == 3*anim_speed:
                if FACING_LEFT:
                    self.image = self.sprites_left[0]
                elif FACING_RIGHT:
                    self.image = self.sprites_right[0]
                self.animation_frame = 0
                
        if self.typ == 1:
        
            anim_speed = 8
            
            for i in range(5):
                
                if self.animation_frame == anim_speed * i:
                    if FACING_LEFT:
                        self.image = self.sprites_left[i]
                    elif FACING_RIGHT:
                        self.image = self.sprites_right[i]
            
            for j, i in enumerate([4,3,2,1]):
                
                if self.animation_frame == anim_speed * (j + 5):
                    if FACING_LEFT:
                        self.image = self.sprites_left[i]
                    elif FACING_RIGHT:
                        self.image = self.sprites_right[i]
                        
            if self.animation_frame == 10*anim_speed:
                if FACING_LEFT:
                    self.image = self.sprites_left[0]
                elif FACING_RIGHT:
                    self.image = self.sprites_right[0]
                self.animation_frame = 0
        
        
            
    
        