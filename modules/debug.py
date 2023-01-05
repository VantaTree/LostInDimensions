import pygame

class Debug:

    def __init__(self, font_size = 18):

        self.screen = pygame.display.get_surface()
        self.surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.debug_list:list = list()
        self.font_size = font_size
        self.font = pygame.font.SysFont("Sitka Small", self.font_size)
        self.on = True

    def __call__(self, name, value):
        if not self.on:return
        
        self.debug_list.append((name, value))

    def draw(self):
        if not self.on:return

        self.screen.blit(self.surface, (0, 0))
        for i, (name, value) in enumerate(self.debug_list):
            text_surf = self.font.render(name + str(value), False, (255,255,255), (0, 0, 0))
            self.screen.blit(text_surf, (10, 10 + (i*(self.font_size+3))))

        self.debug_list.clear()
        self.surface.fill((0, 0, 0, 0))
