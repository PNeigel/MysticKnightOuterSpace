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
from class_enemy import enemy
import time
import tools as tools
from rail_gun import rail_gun
from tesla_coil import tesla_coil
from class_projectile import projectile
import numpy as np

class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.pre_init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((Width, Height))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        
        self.healthbar = pg.image.load('../Gameart/Bars/Healthbar.png')
        self.healthbar = self.healthbar.convert_alpha()
        
        self.dead = False
        
        self.GO_screenA = pg.image.load('../Gameart/Screens/gameoverA.png').convert()
        self.GO_screenA = pg.transform.scale(self.GO_screenA, (settings.Width, settings.Height))
        self.GO_screenB = pg.image.load('../Gameart/Screens/gameoverb.png').convert()
        self.GO_screenB = pg.transform.scale(self.GO_screenB, (settings.Width, settings.Height))
        
        self.hearts = []
        self.hearts.append(pg.image.load('../Gameart/Hud/Heart.png').convert_alpha())
        self.hearts[-1] = pg.transform.scale(self.hearts[-1], (45,45))
        self.hearts.append(pg.image.load('../Gameart/Hud/Heart.png').convert_alpha())
        self.hearts[-1] = pg.transform.scale(self.hearts[-1], (30,30))
        
        self.heart_image = self.hearts[0]
        
        self.path_HP = 100
        
        self.font = pg.font.SysFont("monospace", 38)
        self.font.set_bold(True)
        
        self.coin_images = []
        for i in range(8):
            self.coin_images.append(pg.image.load('../Gameart/Hud/Coin/%d.png' % i).convert_alpha())
            self.coin_images[-1] = pg.transform.scale(self.coin_images[-1], (45,45))
        self.coin_image = self.coin_images[0]
        self.coin_animation_frame = 0
        self.heart_animation_frame = 0
        
        # SOUNDS
        
        self.music = pg.mixer.Sound('../Gameart/Music/Game/game5.ogg')
        self.music.set_volume(0.5)
        self.GO_music = pg.mixer.Sound('../Gameart/Music/Gameover/gameover.ogg')
        self.GO_music.set_volume(0.5)
        self.intrude_sound = pg.mixer.Sound('../Gameart/Sounds/Game/Gamestart/intrude.ogg')
        self.intrude_sound.set_volume(0.5)
        
        self.tesla_sound = pg.mixer.Sound('../Gameart/Sounds/Tower/Shoot/Tesla.wav')
        self.mg_sound = pg.mixer.Sound('../Gameart/Sounds/Tower/Shoot/Rail.wav')
        
        self.etru_sound = pg.mixer.Sound('../Gameart/Sounds/Game/Enemythrough/qubodup-PowerDrain.ogg')
        
        self.intro_music = pg.mixer.Sound('../Gameart/Music/Intro/Menu.ogg')
        
        self.die_anim = False
        
        self.intro_image = pg.image.load('../Gameart/Screens/start.png').convert()
        self.intro_image = pg.transform.scale(self.intro_image, (settings.Width, settings.Height))

    def new(self):
        # start a new game
        self.player = player_character()
        self.camera_x = self.player.x_pos - 300
        self.camera_y = self.player.y_pos - 300
        self.prev_camera_x = self.player.x_pos - 300
        self.prev_camera_y = self.player.y_pos - 300
        self.level = level()
        self.BG_sprites = pg.sprite.Group()
        self.FG_sprites = pg.sprite.Group()
        self.BG_sprites.add(self.level)
        #self.FG_sprites.add(self.player)
        #self.FG_sprites.add(enemy(1435., 1085.))
        
        choice = self.run()
        
        return choice
    
    def run(self):
        # gameloop
        self.intro_music.play()
        self.screen.blit(self.intro_image, (0,0), (0,0, self.intro_image.get_width(), self.intro_image.get_height()))
        while True:
            
            self.clock.tick(FPS)
            
            self.events()
            
            keys = pg.key.get_pressed()
            if keys[loc.K_RETURN]:
                self.intro_music.stop()
                break
            
            pg.display.update()
            
        self.GO_music.stop()
        self.intrude_sound.play()
        self.playing = True
        frames = 0
        timer = pg.time.get_ticks()
        self.ticks = 0
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
            self.ticks += 1
        die_anim_ticks = 0
        print self.die_anim
        while self.die_anim:
            
            ani_speed = 60
            
            for i in range(5):
                
                if die_anim_ticks == ani_speed * i:
                    
                    self.player.image = self.player.die_anim[i]
                    
            self.draw()
            
            die_anim_ticks += 1
            if die_anim_ticks == 600:
                self.dead = True
                break
        self.select_state = 0
        print "going into dead screen"
        choice = self.show_dead_screen()
        print choice
        return choice
            

    def update(self):
        
        if self.ticks == 200:
            self.music.play(loops=-1)
        
        self.coin_animation_frame += 1
        self.heart_animation_frame += 1
        
        # COIN ANIM
        anim_speed = 8
        
        for i in range(8):
            
            if self.coin_animation_frame == anim_speed * i:
                self.coin_image = self.coin_images[i]
                
        if self.coin_animation_frame == 8*anim_speed:
            self.coin_image = self.coin_images[0]
        if self.coin_animation_frame == 12*anim_speed:
            self.coin_animation_frame = 0
            
            
        # HEART ANIM
        anim_speed = 50
        for i in range(2):
            
            if self.heart_animation_frame == anim_speed * i:
                self.heart_image = self.hearts[i]
                
        if self.heart_animation_frame == 2*anim_speed:
            self.heart_animation_frame = -1
        
        # Game Loop - update
        if self.camera_x != self.prev_camera_x or self.camera_y != self.prev_camera_y:
            self.level.update(self.camera_x, self.camera_y)
        self.player.update()
        #self.FG_sprites.update()
        self.update_camera(tools.ScreenFromIngame(self.player.x_pos, self.player.y_pos))
        
        erects = [enemy_.collision_rect for enemy_ in self.FG_sprites]
        
        spawn_x, spawn_y = (1485.,1085.)
        
        # ============ SPAWN ENEMIES
        
        if self.ticks % 2000 == 0 and self.ticks > 0:
            self.FG_sprites.add(enemy(spawn_x, spawn_y, 1))
        elif self.ticks % 200 == 0:
            self.FG_sprites.add(enemy(spawn_x, spawn_y, 0))
        
        for tower in self.player.towers_sprites:
            tower.update()
            if tower.attack_CD == 0:
                idx = tower.attack_rect.collidelist(erects)
                if idx != -1:
                    tower.target = self.FG_sprites.sprites()[idx]
                    if tower.type == 1:
                        tower.projectiles.add(projectile(tower.x_pos, tower.y_pos, tower.target))
                        self.tesla_sound.play()
                    elif tower.type == 0:
                        tower.target.hp -= 10
                        self.mg_sound.play()
        
        hitsoundvals = [0,0]
        for enemy_ in self.FG_sprites:
            if self.player.attacking and self.player.attacking_CD == 20:
                if  self.player.attack_collision_rect.colliderect(enemy_.collision_rect):
                    enemy_.hp -= 30
                    hitsoundvals[0] += 1 
                else:
                    hitsoundvals[1] += 1
            enemy_.update()
            if self.player.collision_rect.colliderect(enemy_.collision_rect):
                if self.player.invincible_frames == 0:
                    self.player.take_damage(enemy_.playerdmg)
                    direc = np.asarray([self.player.x_pos - enemy_.x_pos, self.player.y_pos - enemy_.y_pos])
                    direc /= np.linalg.norm(direc)
                    self.player.x_pos += 100*direc[0]
                    self.player.y_pos += 100*direc[1]
            if self.player.hp <= 0:
                self.die_anim = True
            if enemy_.destroy_flag:
                if enemy_.remove_path_hp:
                    self.path_HP -= enemy_.path_dmg
                    self.etru_sound.play()
                else:
                    self.player.gold += 10
                    print "Gold: %d" % self.player.gold
                self.FG_sprites.remove(enemy_)
        if hitsoundvals[0]:
            self.player.sword_nohit.play()
            self.player.sword_hit.play()
        elif hitsoundvals[1]:
            self.player.sword_nohit.play()
        
        if self.die_anim or self.path_HP <= 0:
            self.playing = False
            
    
    def events(self):
        keys = pg.key.get_pressed()
        if keys[loc.K_ESCAPE]:
            self.playing = False
            self.running = False
            pg.mixer.quit()
            pg.quit()
        if keys[loc.K_p]:
            pg.image.save(self.screen, "screenshot%d.png" % time.time())
        # Game Loop - events
        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
                pg.mixer.quit()
                pg.quit()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(black)
        #self.draw_relative_to_camera(self.screen, self.level)
        self.BG_sprites.draw(self.screen)
        
        for (x,y) in self.level.path:
            x,y = tools.ScreenFromIngame(x,y)
            x = x-int(self.camera_x)
            y = y-int(self.camera_y)
            #tmp_rect = pg.draw.circle(self.screen, settings.white, (x,y) , 10)
            #pg.display.update(tmp_rect)
        
        for enemy_ in self.FG_sprites:
            self.draw_relative_to_camera(self.screen, enemy_)
            
        for tower in self.player.towers_sprites:
            if tower.type == 1:
                for proj in tower.projectiles:
                    self.draw_relative_to_camera(self.screen, proj)
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
        im_width = sprite.image.get_width()
        im_height = sprite.image.get_height()
        surface.blit(sprite.image, (x-im_width/2,y-im_height/2), (0,0, im_width, im_height))
        
    def update_camera(self, player_screen_pos):
        self.prev_camera_x = self.camera_x
        self.prev_camera_y = self.camera_y
        x,y = player_screen_pos
        scrolling_val_x = settings.Width / 3
        scrolling_val_y = settings.Height / 3
        part = 5
        if x <= self.camera_x + settings.Width / part:
            self.camera_x = x - settings.Width / part - scrolling_val_x
        elif x >= self.camera_x + settings.Width * (part - 1) / part:
            self.camera_x = x - settings.Width * (part - 1) / part + scrolling_val_x
        if y <= self.camera_y + settings.Height / part:
            self.camera_y = y - settings.Height / part - scrolling_val_y
        elif y >= self.camera_y + settings.Height * (part - 1) / part:
            self.camera_y = y - settings.Height * (part - 1) / part + scrolling_val_y

    def show_start_screen(self):
        # game splash/start screen
        pass
    
    def show_dead_screen(self):
        self.music.stop()
        self.GO_music.play(loops=-1)
        while self.dead:
            self.clock.tick(FPS)
            self.events()
            keys = pg.key.get_pressed()
            if keys[loc.K_RIGHT]:
                self.select_state = 1
            elif keys[loc.K_LEFT]:
                self.select_state = 0
            self.events()
            keys = pg.key.get_pressed()
            if self.select_state == 0:
                self.screen.blit(self.GO_screenB, (0,0), (0,0,self.GO_screenB.get_width(), self.GO_screenB.get_height()))
                if keys[loc.K_RETURN]:
                    return 0
            elif self.select_state == 1:
                self.screen.blit(self.GO_screenA, (0,0), (0,0,self.GO_screenA.get_width(), self.GO_screenA.get_height()))
                if keys[loc.K_RETURN]:
                    return 1
            pg.display.update()
        
    
    def draw_hud(self):
        # HP
        self.screen.blit(self.healthbar, (10,100), (0,0,50,260))
        h = 227. * self.player.hp / self.player.max_hp
        hp_rect = pg.Rect(21,113-h+227,28,h)
        pg.draw.rect(self.screen, settings.red, hp_rect)
        
        for enemy_ in self.FG_sprites:
            x,y = enemy_.rect.x - enemy_.sprite_width / 2, enemy_.rect.y - enemy_.sprite_width / 2
            x -= self.camera_x
            y -= self.camera_y
            
            if enemy_.typ == 0:
                y -= 30
                #x = enemy_.rect.x
                #y = enemy_.rect.y
                tmprect = pg.Rect(x,y,100,20)
                pg.draw.rect(self.screen, settings.black, tmprect)
                tmprect = pg.Rect(x+1,y+1,(98*enemy_.hp) / enemy_.max_HP,18)
                pg.draw.rect(self.screen, settings.red, tmprect)
            
            if enemy_.typ == 1:    
                y -= 45
                x -= 40
                #x = enemy_.rect.x
                #y = enemy_.rect.y
                tmprect = pg.Rect(x,y,300,20)
                pg.draw.rect(self.screen, settings.black, tmprect)
                tmprect = pg.Rect(x+1,y+1,(298*enemy_.hp) / enemy_.max_HP,18)
                pg.draw.rect(self.screen, settings.red, tmprect)
                
            
        tmprect = pg.Rect(10,10,340, 50)
        pg.draw.rect(self.screen, black, tmprect)
        self.gold_label = self.font.render("%s" % self.player.gold, 1, white)
        self.screen.blit(self.gold_label, (250, 16))
        self.heart_label = self.font.render("%s" % self.path_HP, 1, white)
        self.screen.blit(self.heart_label, (60, 16))
        
        self.screen.blit(self.coin_image, (200, 12), (0,0, self.coin_image.get_width(), self.coin_image.get_height()))
        x = 10+45/2
        y = 12+45/2
        x -= self.heart_image.get_width() / 2
        y -= self.heart_image.get_height() / 2
        self.screen.blit(self.heart_image, (x, y), (0,0, self.heart_image.get_width(), self.heart_image.get_height()))


while True:
    g = Game()
    g.show_start_screen()
    choice = g.new()
    print choice
    if choice == 1:
        pg.mixer.quit()
        pg.quit()
        break
