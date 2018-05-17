import numpy as np
import pygame as pg
import settings as settings
import pygame.locals as loc
import tools as tools
from rail_gun import rail_gun
from tesla_coil import tesla_coil

from class_projectile import projectile

player_width = 110
player_height = 110
min_area = 100

class player_character(pg.sprite.DirtySprite):
    
    def __init__(self):
        super(player_character, self).__init__()
        self.x_pos = 1500.
        self.y_pos = 500.
        self.prev_x = self.x_pos
        self.prev_y = self.y_pos
        self.animation_frame = 0
        #self.source_rect = pg.Rect(0,0,1,1)
        self.spritesheet_right = []
        self.spritesheet_right.append(pg.image.load('../Gameart/Player/Walking/Walking2/Right/standingR.png'))
        self.spritesheet_right[-1] = pg.transform.scale(self.spritesheet_right[-1], (player_width, player_height))
        self.spritesheet_right[-1] = self.spritesheet_right[-1].convert_alpha()
        for i in range(1, 8):
            self.spritesheet_right.append(pg.image.load('../Gameart/Player/Walking/Walking2/Right/walk%dR.png' % i))
            self.spritesheet_right[-1] = pg.transform.scale(self.spritesheet_right[-1], (player_width, player_height))
            self.spritesheet_right[-1] = self.spritesheet_right[-1].convert_alpha()
            
        self.spritesheet_left = []
        self.spritesheet_left.append(pg.image.load('../Gameart/Player/Walking/Walking2/Left/standing.png'))
        self.spritesheet_left[-1] = pg.transform.scale(self.spritesheet_left[-1], (player_width, player_height))
        self.spritesheet_left[-1] = self.spritesheet_left[-1].convert_alpha()
        for i in range(1, 8):
            self.spritesheet_left.append(pg.image.load('../Gameart/Player/Walking/Walking2/Left/walk%d.png' % i))
            self.spritesheet_left[-1] = pg.transform.scale(self.spritesheet_left[-1], (player_width, player_height))
            self.spritesheet_left[-1] = self.spritesheet_left[-1].convert_alpha()
        
        self.sword_right = []
        for i in range(1,5):
            self.sword_right.append(pg.image.load('../Gameart/Player/Sword/Right/sword%dR.png' % i))
            self.sword_right[-1] = pg.transform.scale(self.sword_right[-1], (2*player_width, 2*player_height))
            self.sword_right[-1] = self.sword_right[-1].convert_alpha()
            
        self.sword_left = []
        for i in range(1,5):
            self.sword_left.append(pg.image.load('../Gameart/Player/Sword/Left/sword%d.png' % i))
            self.sword_left[-1] = pg.transform.scale(self.sword_left[-1], (2*player_width, 2*player_height))
            self.sword_left[-1] = self.sword_left[-1].convert_alpha()
            
        self.die_anim = []
        for i in range(1,6):
            self.die_anim.append(pg.image.load('../Gameart/Player/Dying/die%d.png' % i).convert_alpha())
        
        self.die_anim[0] = pg.transform.scale(self.die_anim[0], (int(2*player_width), int(2*player_height)))
        self.die_anim[1] = pg.transform.scale(self.die_anim[1], (int(3*player_width), int(3*player_height)))
        self.die_anim[2] = pg.transform.scale(self.die_anim[2], (int(4*player_width), int(4*player_height)))
        self.die_anim[3] = pg.transform.scale(self.die_anim[3], (int(3*player_width), int(3*player_height)))
        self.die_anim[4] = pg.transform.scale(self.die_anim[4], (int(2*player_width), int(2*player_height)))
        
        self.image = self.spritesheet_right[0]
        #self.image = pg.Surface((player_width, player_height))
        #self.image.set_colorkey(settings.alpha_pink)
        #self.image.blit(self.spritesheet[], (0,0), (0, 0, 100, 100))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        #self.rect = pg.Rect(0, 0, 100, 100)
        #self.image = pg.Surface([player_width, player_height])
        #self.image.fill(settings.blue)
        self.walking = True
        self.projectiles = pg.sprite.Group()
        self.max_hp = 100
        self.hp = self.max_hp
        self.collision_radius = 10
        self.collision_rect = pg.Rect(self.x_pos-self.collision_radius, self.y_pos-self.collision_radius, 2*self.collision_radius, 2*self.collision_radius)
        
        self.attack_radius = 50
        self.attack_collision_rect = pg.Rect(self.x_pos-self.attack_radius, self.y_pos-self.attack_radius, 2*self.attack_radius, 2*self.attack_radius)
        self.invincible_frames = 0
        self.facing = 'right'
        self.attacking = False
        self.attacking_CD = 0
        
        # Init towers
        self.towers_sprites = pg.sprite.Group()
        
        self.dir = np.ones(2)
        
        self.gold = 40
        
        self.build_CD = 0
        
        ### SOUNDS
        
        self.sword_nohit = pg.mixer.Sound('../Gameart/Sounds/Player/Sword/swing.wav')
        self.sword_nohit.set_volume(0.5)
        self.sword_hit = pg.mixer.Sound('../Gameart/Sounds/Player/Hurt/hurt1.wav')
        self.sword_hit.set_volume(1.0)
        self.take_damage_sound = pg.mixer.Sound('../Gameart/Sounds/ZSource/argh/aargh3.ogg')
        self.take_damage_sound.set_volume(0.5)
        self.death_sound = pg.mixer.Sound('../Gameart/Sounds/Player/die/die.ogg')
        
        self.build_sound = pg.mixer.Sound('../Gameart/Sounds/Tower/Build/build.ogg')
        self.nobuild_sound = pg.mixer.Sound('../Gameart/Sounds/Tower/Build/nobuild1.wav')
        
    def update(self):
        
        # TICK STUFF
        self.prev_x = self.x_pos
        self.prev_y = self.y_pos
        if self.invincible_frames > 0:
            self.invincible_frames -= 1
        if self.attacking_CD > 0:
            self.attacking_CD -= 1
            
        if self.build_CD > 0:
            self.build_CD -= 1
            
        self.attack_collision_rect.x = self.x_pos - self.attack_radius
        self.attack_collision_rect.y = self.y_pos - self.attack_radius
        
        # ANIMATE
        if self.walking:
            self.attacking = False
            length = 2
            for i in range(8):
                if self.animation_frame in range(i*length, (i+1)*length):
                    if self.facing is 'left':
                        self.image = self.spritesheet_left[i]
                    else:
                        self.image = self.spritesheet_right[i]
                    self.animation_frame += 1
                    break
            if self.animation_frame == 8*length:
                self.animation_frame = 0
                if self.facing is 'left':
                    self.image = self.spritesheet_left[0]
                else:
                    self.image = self.spritesheet_right[0]
        elif self.attacking:
            self.rect.x -= 50
            self.rect.y -= 50
            self.walking = False
            length = 4
            for i in range(4):
                if self.animation_frame in range(i*length, (i+1)*length):
                    if self.facing is 'left':
                        pass
                        self.image = self.sword_left[i]
                    else:
                        self.image = self.sword_right[i]
                    self.animation_frame += 1
                    break
            if self.animation_frame == 4*length:
                self.animation_frame = 0
                self.attacking = False
                if self.facing is 'left':
                    self.image = self.spritesheet_left[0]
                else:
                    self.image = self.spritesheet_right[0]
                
        else:
            if self.facing is 'left':
                self.image = self.spritesheet_left[0]
            else:
                self.image = self.spritesheet_right[0]
                
        # MOVE
        keys = pg.key.get_pressed()
        speed = 3.
        
        if keys[loc.K_RIGHT]:
            self.x_pos += speed
            self.y_pos -= speed
            self.walking = True
            self.facing = 'right'
        elif keys[loc.K_LEFT]:
            self.x_pos -= speed
            self.y_pos += speed
            self.walking = True
            self.facing = 'left'
        if keys[loc.K_UP]:
            self.x_pos -= speed
            self.y_pos -= speed
            self.walking = True
        elif keys[loc.K_DOWN]:
            self.x_pos += speed
            self.y_pos += speed
            self.walking = True
        
        new_dir = np.asarray([self.x_pos - self.prev_x, self.y_pos - self.prev_y])
        if np.any(new_dir):
            self.dir = new_dir
            self.dir /= np.linalg.norm(self.dir)
        self.rect.x, self.rect.y = tools.ScreenFromIngame(self.x_pos, self.y_pos)
        
        #if self.attacking:
        #    self.rect.x -= 50
        #    self.rect.y -= 50
        
        self.collision_rect.x = self.x_pos - self.collision_radius
        self.collision_rect.y = self.y_pos - self.collision_radius
        
        if not np.any([keys[i] for i in [loc.K_RIGHT, loc.K_LEFT, loc.K_UP, loc.K_DOWN]]):
            self.walking = False
        
        if keys[loc.K_SPACE] and self.attacking_CD == 0:
            self.attacking = True
            self.animation_frame = 0
            self.attacking_CD = 20
            print self.x_pos, self.y_pos
            
        # place rail_gun
        if keys[loc.K_1] and self.build_CD == 0:
            if self.check4towers(0) and self.gold >= 40:
                self.towers_sprites.add(rail_gun(self.x_pos, self.y_pos))
                self.gold -= 40
                print "Gold: %d" % self.gold
                self.build_sound.play()
                self.build_CD = 40
            else:
                self.nobuild_sound.play()
                

        # place tesla_coil
        if keys[loc.K_2] and self.build_CD == 0:
            if self.check4towers(50) and self.gold >= 80:
                self.towers_sprites.add(tesla_coil(self.x_pos, self.y_pos))
                self.gold -= 80
                print "Gold: %d" % self.gold
                self.build_sound.play()
                self.build_CD = 40
            else:
                self.nobuild_sound.play()
            
    def check4towers(self, bias):
        for tower in self.towers_sprites:
            d = max(np.abs(tower.x_pos - self.x_pos),
                    np.abs(tower.y_pos - self.y_pos))
            if d < min_area + bias:
                return False
        return True
    
    def take_damage(self, damage):
        if self.invincible_frames == 0:
            if self.hp > 0:
                if self.hp <= damage:
                    self.hp = -1
                    self.death_sound.play()
                else:
                    self.hp -= damage
                    self.take_damage_sound.play()
            self.invincible_frames = 30
    
        