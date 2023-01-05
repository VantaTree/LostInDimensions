import pygame

class Game:

    def __init__(self, master):

        self.master = master
        self.master.game = self
        self.screen = pygame.display.get_surface()

    def run(self):

        self.screen.fill("turquoise")
        pass
