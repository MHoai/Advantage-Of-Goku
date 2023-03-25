import pygame
from support import import_folder

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, surface, shift):
        super().__init__()
        #set initial status
        self.pos = pos
        self.isAvaiable = True
        self.shift = shift
      #  print(self.shift)
        
        self.image = surface
        self.rect = self.image.get_rect(center = pos)

        self.flip()
        
    def flip(self):
        if self.shift < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
    def update(self, player):
        self.rect.x += self.shift
