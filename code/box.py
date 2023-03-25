import pygame, time
from tile import  AnimatedTile
from random import randint
from settings import *
from support import import_folder

class Box_Animated(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../graphics/box/box_static')
        self.rect.y += size - self.image.get_size()[1]
        self.gift = randint(1,5)
        self.be_hited = False
        self.pass_time = 0
            
    def update(self,shift):##################################
        self.rect.x += shift
        if(self.be_hited):
            if self.gift == 1 :
                self.frames = import_folder('../graphics/box/box_hp')
            elif self.gift == 2 :
                self.frames = import_folder('../graphics/box/box_mana')
            else  :
                self.frames = import_folder('../graphics/box/box_free')  
                
        self.animate()
       # self.healthBar.update()###########################