import pygame, time ##################################
from settings import *
class manaBar(pygame.sprite.Sprite):
    def __init__(self, width, height, mana):
        super().__init__()
        self.width = width
        self.height = height
        self.mana = mana
        self.image = pygame.Surface((self.width, self.height))
        self.pass_time = pygame.time.get_ticks()
       # self.image.fill((0, 255, 0))
            
    def draw(self, screen, character_rect):
        #health_rect.move_ip(self.x, self.y)
        health_rect = pygame.Rect(0, 0, self.width * (self.mana / mana), self.height*(1/2))
        health_border_rect = pygame.Rect(0, 0, self.width + 2, self.height*(1/2)+2)
        health_rect.topleft = (character_rect.x, character_rect.y - 15)
        health_border_rect.topleft = (character_rect.x - 1, character_rect.y - 15 - 1)
        pygame.draw.rect(screen, (0, 0, 255), health_rect)
        pygame.draw.rect(screen, (0, 0, 0), health_border_rect,2)
