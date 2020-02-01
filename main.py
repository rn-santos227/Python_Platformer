import pygame as pg
import random
from setting import *
from sprites import *
from platforms import *

class Game:
    def __init__(self):
        #initialize window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        #start new game
        self.all_sprites = pg.sprite.Group() 
        self.platforms = pg.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player) 

        for platform in PLATFORM_LIST:
            a = Platform(*platform)
            self.all_sprites.add(a)
            self.platforms.add(a)

        self.run()


    def run(self):
        #game loop
        self.playing = True
        while self.playing: 
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #game loop - update
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if self.player.vel.y > 0:
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.rect.midbottom = self.player.pos

        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for platform in self.platforms:
                platform.rect.y += abs(self.player.vel.y)
                if platform.rect.top >= HEIGHT:
                    platform.kill()

        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
            self.playing = False

        while len(self.platforms) < 6:
            width = random.randrange(100, 200)
            p = Platform(random.randrange(0, WIDTH-width), random.randrange(-30, -25), width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        #game loop - events
        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
    
    def draw(self):
        #game loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()
while g.running: 
    g.new()
    g.show_go_screen()

pg.quit()