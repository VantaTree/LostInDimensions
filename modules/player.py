import pygame
import random
from .frect import FRect
from .engine import *
from .config import *

class Player:

    def __init__(self, master):

        self.master = master
        self.master.player = self
        self.screen = pygame.display.get_surface()

        self.original_image = pygame.image.load("graphics/player/test.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.slant_rect = pygame.Rect(0, 0, 16, 3)
        self.hitbox = FRect(0, 0, 16, 32)
        self.velocity = pygame.Vector2()
        self.input_x = 0
        self.max_speed = 2
        self.acceleration = 0.5
        self.deceleration = 0.5
        self.jump_power = 7.5
        self.gravity = 0.5

        self.facing_right = True
        self.moving = False
        self.can_jump = True
        self.on_ground = True

        self.JUMP_TIMER = CustomTimer()

    def update_image(self):

        self.image = pygame.transform.flip(self.original_image, self.facing_right, False)
        self.rect.midbottom = self.hitbox.midbottom

    def get_input(self):

        keys = pygame.key.get_pressed()

        self.input_x = 0
        if keys[pygame.K_d]:
            self.input_x += 1
            self.facing_right = True
        if keys[pygame.K_a]:
            self.input_x -= 1
            self.facing_right = False
        
        if keys[pygame.K_SPACE] and self.on_ground and self.can_jump:

            self.velocity.y = -self.jump_power
            self.can_jump = False
            self.JUMP_TIMER.start(100)

        self.moving = bool(self.input_x)

    def apply_force(self):

        if self.moving:
            self.velocity.move_towards_ip( (self.max_speed*self.input_x, self.velocity.y), self.acceleration *self.master.dt)
        else:
            self.velocity.move_towards_ip( (0, self.velocity.y), self.deceleration *self.master.dt)

        self.velocity.y += self.gravity *self.master.dt
        if self.velocity.y > 8:
            self.velocity.y = 8

    def move(self):

        self.hitbox.centerx += self.velocity.x * self.master.dt
        do_collision(self, self.master.game.level, 0, self.master)
        self.hitbox.centery += self.velocity.y * self.master.dt
        self.on_ground = False
        do_collision(self, self.master.game.level, 1, self.master)
        do_collision(self, self.master.game.level, 2, self.master)

    def process_events(self):

        for event in pygame.event.get(()):
            pass

        if self.JUMP_TIMER.check():
            self.can_jump = True

    def draw(self):

        self.screen.blit(self.image, self.rect.topleft + self.master.offset)

    def update(self):

        self.process_events()
        self.get_input()
        self.apply_force()
        self.move()
        self.update_image()

def do_collision(player:Player, level, axis, master):

    px = int(player.hitbox.centerx / TILESIZE)
    py = int(player.hitbox.centery / TILESIZE)
    player.slant_rect.midbottom = player.hitbox.midbottom

    for y in range(py-1, py+2):
        for x in range(px-1, px+2):

            if x < 0 or y < 0: continue

            rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
            if not player.hitbox.colliderect(rect): continue

            if axis == 0: # x-axis

                if get_xy(level.wall_coll, x, y):

                    if player.velocity.x > 0:
                        player.hitbox.right = rect.left
                    if player.velocity.x < 0:
                        player.hitbox.left = rect.right

            elif axis == 1: # y-axis

                if get_xy(level.ground_coll, x, y):

                    if rect.collidepoint(player.hitbox.bottomleft) or\
                        rect.collidepoint(player.hitbox.bottomright):
                    # if rect.colliderect(player.slant_rect):

                        if player.velocity.y > 0:
                            player.hitbox.bottom = rect.top
                            player.velocity.y = 0
                            player.on_ground = True

                if get_xy(level.ceil_coll, x, y):
                    if player.velocity.y < 0:
                        player.hitbox.top = rect.bottom
                        player.velocity.y = 0

            elif axis == 2 and player.velocity.y >= 0: # slopes

                if not rect.colliderect(player.slant_rect): continue
                # if not rect.collidepoint(player.hitbox.bottomleft) and not\
                #         rect.collidepoint(player.hitbox.bottomright):continue


                if get_xy(level.up_slant_coll, x, y):
                    relx = player.hitbox.right - rect.left
                    if relx > TILESIZE:
                        player.hitbox.bottom = rect.top
                        player.on_ground = True
                        player.velocity.y = 0
                    elif player.hitbox.bottom > y*TILESIZE-relx+TILESIZE:
                        player.hitbox.bottom = y*TILESIZE-relx+TILESIZE
                        player.on_ground = True
                        player.velocity.y = 0

                if get_xy(level.down_slant_coll, x, y):
                    relx = rect.right - player.hitbox.left
                    master.debug("On slope: ", True)
                    if relx > TILESIZE:
                        player.hitbox.bottom = rect.top
                        player.on_ground = True
                        player.velocity.y = 0
                    if player.hitbox.bottom > y*TILESIZE-relx+TILESIZE:
                        player.hitbox.bottom = y*TILESIZE-relx+TILESIZE
                        player.on_ground = True
                        player.velocity.y = 0
                        
def get_xy(grid, x, y):

    if x < 0 or y < 0: return
    try:
        return grid[y][x]
    except IndexError: return