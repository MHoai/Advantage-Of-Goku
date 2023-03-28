import pygame, time
from tile import  AnimatedTile
from settings import *
from support import import_folder

class Super_Box_Animated(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../graphics/box/box_static')
        self.rect.y += size - self.image.get_size()[1]
        self.be_hited = False
        self.pass_time = 0
            
    def update(self, shift_x, shift_y):##################################
        self.rect.x += shift_x
        self.rect.y += shift_y
        if(self.be_hited):
                self.frames = import_folder('../graphics/super box')  
                
        self.animate()
       # self.healthBar.update()###########################