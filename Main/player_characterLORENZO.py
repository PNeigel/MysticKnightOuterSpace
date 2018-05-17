import numpy as np
import pygame as pg
import settings as settings
import pygame.locals as loc
import tools as tools

from rail_gun import rail_gun
from tesla_coil import tesla_coil

from class_projectile import projectile

player_width = 100
player_height = 100
min_area = 100

class player_character(pg.sprite.DirtySprite):

    def __init__(self):
        super(player_character, self).__init__()
        self.x_pos = 0.
        self.y_pos = 0.
        self.prev_x = self.x_pos
        self.prev_y = self.y_pos
        self.animation_frame = 0
        #self.source_rect = pg.Rect(0,0,1,1)
        self.spritesheet_right = []
        self.spritesheet_right.append(pg.image.load('../Gameart/Player/Walking/Walking1/Right/standingR.png'))
        self.spritesheet_right[-1] = pg.transform.scale(self.spritesheet_right[-1], (player_width, player_height))
        self.spritesheet_right[-1] = self.spritesheet_right[-1].convert_alpha()
        for i in range(1, 8):
            self.spritesheet_right.append(pg.image.load('../Gameart/Player/Walking/Walking1/Right/walk%dR.png' % i))
            self.spritesheet_right[-1] = pg.transform.scale(self.spritesheet_right[-1], (player_width, player_height))
            self.spritesheet_right[-1] = self.spritesheet_right[-1].convert_alpha()

        self.spritesheet_left = []
        self.spritesheet_left.append(pg.image.load('../Gameart/Player/Walking/Walking1/Left/standing.png'))
        self.spritesheet_left[-1] = pg.transform.scale(self.spritesheet_left[-1], (player_width, player_height))
        self.spritesheet_left[-1] = self.spritesheet_left[-1].convert_alpha()
        for i in range(1, 8):
            self.spritesheet_left.append(pg.image.load('../Gameart/Player/Walking/Walking1/Left/walk%d.png' % i))
            self.spritesheet_left[-1] = pg.transform.scale(self.spritesheet_left[-1], (player_width, player_height))
            self.spritesheet_left[-1] = self.spritesheet_left[-1].convert_alpha()
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
        self.collision_rect = pg.Rect(self.x_pos, self.y_pos, 100, 100)
        self.invincible_frames = 0
        self.facing = 'right'

        # Init towers
        self.towers_sprites = pg.sprite.Group()

    def update(self):

        # TICK STUFF
        self.prev_x = self.x_pos
        self.prev_y = self.y_pos
        if self.invincible_frames > 0:
            self.invincible_frames -= 1

        # ANIMATE
        if self.walking:
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
        self.dir = np.asarray([self.x_pos - self.prev_x, self.y_pos - self.prev_y])
        self.rect.x, self.rect.y = tools.ScreenFromIngame(self.x_pos, self.y_pos)
        self.collision_rect.x = self.x_pos
        self.collision_rect.y = self.y_pos

        if not np.any([keys[i] for i in [loc.K_RIGHT, loc.K_LEFT, loc.K_UP, loc.K_DOWN]]):
            self.walking = False

        if keys[loc.K_SPACE]:
            print self.x_pos, self.y_pos
            #self.projectiles.add(projectile((1,1)))

        # place rail_gun
        if keys[loc.K_1] and self.check4towers(0):
            self.towers_sprites.add(rail_gun(self.x_pos, self.y_pos))

        # place tesla_coil
        if keys[loc.K_2] and self.check4towers(50):
            self.towers_sprites.add(tesla_coil(self.x_pos, self.y_pos))

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
                self.hp -= min(damage, self.hp)
            self.invincible_frames = 30
