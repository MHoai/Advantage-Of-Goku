import pygame, time ##################################
from settings import *
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, width, height, health):
        super().__init__()
        self.width = width
        self.height = height
        self.health = health
        self.image = pygame.Surface((self.width, self.height))
       # self.image.fill((0, 255, 0))

    def draw(self, screen, character_rect, type):
        #health_rect.move_ip(self.x, self.y)
        if(type =='player') :
          health_rect = pygame.Rect(0, 0, self.width * (self.health / hpPlayer), self.height)
          health_border_rect = pygame.Rect(0, 0, self.width + 2, self.height+2)
          health_rect.topleft = (character_rect.x, character_rect.y - 30)
          health_border_rect.topleft = (character_rect.x - 1, character_rect.y - 30 - 1)
          pygame.draw.rect(screen, (0, 255, 0), health_rect)
          pygame.draw.rect(screen, (0, 0, 0), health_border_rect,2)
        elif(type =='enemy') :  
          health_rect = pygame.Rect(0, 0, self.width * (self.health / hpEnemy), self.height)
          health_border_rect = pygame.Rect(0, 0, self.width + 2, self.height+2)
          health_rect.topleft = (character_rect.x, character_rect.y - 30)
          health_border_rect.topleft = (character_rect.x - 1, character_rect.y - 30 - 1)
          pygame.draw.rect(screen, yellow, health_rect)
          pygame.draw.rect(screen, (0, 0, 0), health_border_rect,2)
        elif(type =='boss') :  
          health_rect = pygame.Rect(0, 0, self.width * (self.health / hpBoss), self.height)
          health_border_rect = pygame.Rect(0, 0, self.width + 2, self.height+2)
          health_rect.topleft = (character_rect.x+30, character_rect.y - 30)######################################
          health_border_rect.topleft = (character_rect.x+30 - 1, character_rect.y - 30 - 1)######################################
          pygame.draw.rect(screen, yellow, health_rect)############################################
          pygame.draw.rect(screen, (0, 0, 0), health_border_rect,2)

    #def update(self):
    #    self.health += changeHP
      
        
