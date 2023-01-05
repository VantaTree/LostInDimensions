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

        self.hitbox = FRect(0, 0, 16, 32)
        self.velocity = pygame.Vector2()
        self.input_x = 0
        self.max_speed = 2
        self.acceleration = 0.1
        self.deceleration = 0.1
        self.jump_power = 6
        self.gravity = 0.1

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
            self.velocity.move_towards_ip( (self.max_speed*self.input_x, self.velocity.y), self.acceleration)
        else:
            self.velocity.move_towards_ip( (0, self.velocity.y), self.deceleration)

        # self.velocity.y += self.gravity

    def move(self):

        self.hitbox.centerx += self.velocity.x * self.master.dt
        self.hitbox.centery += self.velocity.y * self.master.dt

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

def do_collision(player, level, axis):

    if axis == 0:
        pass