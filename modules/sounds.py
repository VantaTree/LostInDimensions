from os import listdir
import pygame

class SoundSet:

    def __init__(self, master):

        self.dict = {}
        
        self.master = master
        self.master.sounds = self.dict

        for sound_file in listdir("sounds"):
            self.dict[sound_file[:-4]] = pygame.mixer.Sound(F"sounds/{sound_file}")
        