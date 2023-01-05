import pygame
import csv
from .config import *
from .engine import *

MAP_CONFIG = {
    "rocky_test":{
        "size": (48, 16),
        "start_pos" : (32, 207),
    }
}

class Level:

    def __init__(self, master, map_type):
        
        self.master = master
        self.screen = pygame.display.get_surface()
        
        self.map_type = map_type
        self.size = MAP_CONFIG[map_type]["size"]
        self.start_pos = MAP_CONFIG[map_type]["start_pos"]

        self.map_surf = pygame.image.load(F"graphics/maps/{map_type}.png")
        self.collision = self.load_csv(F"data/maps/{map_type}/collision.csv", True)
        self.up_slant_coll = self.load_csv(F"data/maps/{map_type}/up_slant_coll.csv", True)
        self.down_slant_coll = self.load_csv(F"data/maps/{map_type}/down_slant_coll.csv", True)

    @staticmethod
    def load_csv(path, integer=False):

        reader = csv.reader(open(path))
        if integer:
            grid = []
            for row in reader:
                grid.append( [int(cell) for cell in row] )
        else:
            grid = [row for row in reader]

        return grid

    def snap_offset(self):

        self.master.offset =  (self.master.player.hitbox.center - pygame.Vector2(W/2, H/2)) * -1

    def update_offset(self):

        camera_rigidness = 0.18 if self.master.player.moving else 0.05
        self.master.offset -= (self.master.offset + (self.master.player.hitbox.center - pygame.Vector2(W/2, H/2)))\
            * camera_rigidness * self.master.dt

    def clamp_offset(self):

        if self.master.offset.x > 0: self.master.offset.x = 0
        elif self.master.offset.x < -self.size[0]*TILESIZE + W:
            self.master.offset.x = -self.size[0]*TILESIZE + W

        # if self.master.offset.y > 0: self.master.offset.y = 0
        if self.master.offset.y < -self.size[1]*TILESIZE + H:
            self.master.offset.y = -self.size[1]*TILESIZE + H

    def transition_to(self):

        self.master.player.hitbox.midbottom = self.start_pos

        self.snap_offset()
        self.clamp_offset()

    def draw_bg(self):

        self.screen.blit(self.map_surf, self.master.offset)

    def draw_fg(self):

        pass

    def update(self):

        self.update_offset()
        self.clamp_offset()
