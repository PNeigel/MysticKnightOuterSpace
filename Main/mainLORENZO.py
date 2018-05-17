# Jumpy! - platform game

import sys
#sys.path.append(r'C:\Users\Hendrik\Desktop\Python')
import pygame as pg
import random
from settings import *
import settings as settings
import pygame.locals as loc
from class_level import level
from player_character import player_character
from rail_gun import rail_gun
from tesla_coil import tesla_coil
from class_enemy import enemy
import time
import tools as tools

class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((Width, Height))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.camera_x = 0.
        self.camera_y = 0.
        self.prev_camera_x = 0.
        self.prev_camera_y = 0.

        self.healthbar = pg.image.load('../Gameart/Bars/Healthbar.png')
        self.healthbar = self.healthbar.convert_alpha()

        self.dead = False

    def new(self):
        # start a new game
        self.player = player_character()
        self.level = level()
        self.BG_sprites = pg.sprite.Group()
        self.FG_sprites = pg.sprite.Group()
        self.BG_sprites.add(self.level)
        #self.FG_sprites.add(self.player)
        self.FG_sprites.add(enemy(1435., 1085.))

        self.run()

    def run(self):
        # gameloop
        self.playing = True
        frames = 0
        timer = pg.time.get_ticks()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            frames += 1.0
            if frames == 100:
                frames = 1
                timer = pg.time.get_ticks()
            pg.display.set_caption(TITLE + "   FPS: " + repr(1000/((pg.time.get_ticks()+1-timer)/frames)))


    def update(self):
        # Game Loop - update
        if self.camera_x != self.prev_camera_x or self.camera_y != self.prev_camera_y:
            self.level.update(self.camera_x, self.camera_y)
        self.player.update()
        self.FG_sprites.update()
        self.update_camera(tools.ScreenFromIngame(self.player.x_pos, self.player.y_pos))

        for tower in self.player.towers_sprites:
            tower.update()

        for enemy in self.FG_sprites:
            if self.player.collision_rect.colliderect(enemy.collision_rect):
                self.player.take_damage(10)
            if self.player.hp <= 0:
                self.dead = True
        if self.dead:
            self.playing = False

    def events(self):
        keys = pg.key.get_pressed()
        if keys[loc.K_ESCAPE]:
            self.playing = False
            self.running = False
        # Game Loop - events
        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(black)
        #self.draw_relative_to_camera(self.screen, self.level)
        self.BG_sprites.draw(self.screen)

        for (x,y) in self.level.path:
            x,y = tools.ScreenFromIngame(x,y)
            x = x-self.camera_x
            y = y-self.camera_y
            tmp_rect = pg.draw.circle(self.screen, settings.white, (x,y) , 10)
            pg.display.update(tmp_rect)

        for enemy_ in self.FG_sprites:
            self.draw_relative_to_camera(self.screen, enemy_)

        for tower in self.player.towers_sprites:
            self.draw_relative_to_camera(self.screen, tower)

        self.draw_relative_to_camera(self.screen, self.player)

        self.draw_hud()
        #self.FG_sprites.draw(self.screen)
        #self.player.projectiles.draw(self.screen)
        pg.display.update()

    def draw_relative_to_camera(self, surface, sprite):
        x,y = sprite.rect.x, sprite.rect.y
        x -= self.camera_x
        y -= self.camera_y
        surface.blit(sprite.image, (x,y), (0,0, sprite.image.get_width(), sprite.image.get_height()))

    def update_camera(self, player_screen_pos):
        self.prev_camera_x = self.camera_x
        self.prev_camera_y = self.camera_y
        x,y = player_screen_pos
        if x <= self.camera_x + settings.Width / 3:
            self.camera_x = x - settings.Width / 3
        elif x >= self.camera_x + settings.Width * 2 / 3:
            self.camera_x = x - settings.Width * 2 / 3
        if y <= self.camera_y + settings.Height / 3:
            self.camera_y = y - settings.Height / 3
        elif y >= self.camera_y + settings.Height * 2 / 3:
            self.camera_y = y - settings.Height * 2 / 3

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_dead_screen(self):
        self.screen.fill(black)

    def draw_hud(self):
        # HP
        self.screen.blit(self.healthbar, (10,100), (0,0,50,260))
        h = 227. * self.player.hp / self.player.max_hp
        hp_rect = pg.Rect(21,113-h+227,28,h)
        pg.draw.rect(self.screen, settings.red, hp_rect)



g = Game()
g.show_start_screen()
g.new()
frames = 0
timer = time.time()
#while g.running:
#    #g.update()
#    frames += 1
#    g.show_go_screen()
#    #pg.display.set_caption("hallo")

pg.quit()
print frames / (time.time() - timer)
