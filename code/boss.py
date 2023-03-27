import pygame
from support import import_folder
from  HealthBar import * 
from  manaBar import *
from settings import * 

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        
        self.rect = self.image.get_rect(center = (x, y))
        
        #position of the boss
        self.x = x
        self.y = y

        # boss status
        self.status = "idle"
        self.facing_right = True
        self.hiting_player = False
        self.can_move = True
        self.time_take_hit = 0###############
        
        #boss atribute
        self.speed = 5
        self.healthBar =  HealthBar(  widthHealthBar_player, heightHealthBar, hpBoss)       


    def import_character_assets(self):
        character_path = '../graphics/demon/individual sprites/'
        self.animations = {'idle':[],'walk':[],'take hit':[],'death':[], 'cleave':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

        
    def animate(self):
        current_time = pygame.time.get_ticks()
        animation = self.animations[self.status]

		# loop over frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "cleave":
                self.hiting_player = True
            if self.status == "death":
                self.kill()
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
            
        self.rect = self.image.get_rect(center = self.rect.center)
            
    def update(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y
        self.animate()
        
        
        