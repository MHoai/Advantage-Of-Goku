import pygame
from support import import_csv_layout, import_cut_graphic
from settings import *
from tile import Tile, StaticTile, AnimatedTile, Coin
from enemy import Enemy
from player import Player
from particles import ParticleEffect
from bullet import Bullet
from box import *#######################

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None
        
        #player
        player_layout = import_csv_layout(level_data['players'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.ball = pygame.sprite.Group()
        self.player_setup(player_layout)
        
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        
        
        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        # coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')
        
        #enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')    
        #constraint    
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')   
        
        #box 
        box_layout = import_csv_layout(level_data['boxs'])
        self.box_sprites = self.create_tile_group(box_layout, 'boxs') 
        
        #barrier
#       barrier_layout = import_csv_layout(level_data['barriers'])
#       self.barrier_sprites = self.create_tile_group(barrier_layout, 'barriers') 

    
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('../graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size,x,y,'../graphics/coins/gold')
                        if val == '1': sprite = Coin(tile_size,x,y,'../graphics/coins/silver')
                        
                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)
                    
                    if type == 'boxs':
                        sprite = Box_Animated(tile_size, x, y)
                        
                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)  
                    
 #                   if type == 'barriers':
 #                       tile_surface = import_cut_graphic('../??/barrier.png')
 #                       sprite = StaticTile(tile_size, x, y, tile_surface)                  
                    
                    sprite_group.add(sprite)    
                        
        return sprite_group
    
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x,y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)
                    
    
    def enemy_collision_reserse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()
    
    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)
#    def barrier_collision(self):
#         player = self.player.sprite################################################
#         collidable_sprites = self.barrier_sprites.sprites()############################################### 
#         if(player.killed_boss):
#             for sprite in collidable_sprites: #################################
#                if sprite.rect.colliderect(player):#############################  
#                    collidable_sprites.kill()
#                    return True
#
#   def checkEndgame():##############################
#        if barrier_collision():  endGame()  #############################          
        
    def box_collision(self):#########################################
         player = self.player.sprite################################################
         collidable_sprites = self.box_sprites.sprites()###############################################
         for sprite in collidable_sprites: #################################
             if sprite.rect.colliderect(player):#############################
                     player.canmove = False
                     sprite.be_hited = True###################################
                     if sprite.pass_time == 0 :## chi cap nhat gift cho lan dau tien#######################################################
                         sprite.pass_time = pygame.time.get_ticks() #######################
                         if(sprite.gift == 1) : ########################################
                            if player.healthBar.health + addHp <= 100 :############################
                                player.healthBar.health += addHp####################
                            else: player.healthBar.health = 100###########################
                            print('hp')
                         elif(sprite.gift == 2) : ####################################33
                            if player.manaBar.mana + addMana <= 100 :#########################
                                player.manaBar.mana += addMana################################################
                            else: player.manaBar.mana = 100#################################   
                            print('mana')              
                     if sprite.pass_time :#########################################################
                         if pygame.time.get_ticks()-sprite.pass_time>=1000 :###############################
                            sprite.kill()############################################     
                            player.canmove = True     
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() #+ self.crate_sprites.sprites()
        collidable_enemy = self.enemy_sprites.sprites() #########################################
        
        for sprite in collidable_sprites: 
            for ball in self.ball:####################################
                if sprite.rect.colliderect(ball):##################
                    ball.kill()###############################
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        for sprite in collidable_enemy: ##########################################
            for ball in self.ball:####################################
                if sprite.rect.colliderect(ball):##################
                    sprite.healthBar.health += DAMAGE_POWER #################################
                    ball.kill()###############################
            if sprite.rect.colliderect(player.rect):#########################3
                if player.direction.x < 0: ###############################
                    player.rect.left = sprite.rect.right#################################3
                    player.on_left = True#################################33
                    self.current_x = player.rect.left#############################
                    if(sprite.can_reverse):########################
                        if(sprite.speed >0): ###########################
                            sprite.reverse()#############################
                            sprite.can_reverse = False##################
                elif player.direction.x > 0:##################################
                    player.rect.right = sprite.rect.left########################3
                    player.on_right = True####################################
                    self.current_x = player.rect.right###############################
                    if(sprite.can_reverse):###########################
                        if(sprite.speed <0): #####################################
                            sprite.reverse()###############
                            sprite.can_reverse = False#################
                else: ##############################################
                    if(sprite.can_reverse):###########################
                        sprite.reverse()##################
                if(player.status=='hit'):#####################
                    if(sprite.be_hited):####################
                        sprite.healthBar.health +=DAMAGE_HIT####################
                        if(player.mana+hit_to_add_mana<=100): player.mana += hit_to_add_mana
                        sprite.be_hited = False#############################
                else:##########################
                    if(player.be_bited):####################
                        player.healthBar.health +=DAMAGE_BITE #########################################
                        player.be_bited = False####################
            else: ################################
                player.be_bited = True ##########################
                sprite.be_hited = True ###########################
                sprite.can_reverse = True ######################################
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() #+ self.crate_sprites.sprites()
        collidable_enemy = self.enemy_sprites.sprites()###################################

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                player.on_enemy = False
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        for sprite in collidable_enemy:###########################################################
            if sprite.rect.colliderect(player.rect):########################
                if player.direction.y > 1: ################################################
                   player.rect.bottom = sprite.rect.top###############################
                   player.direction.y = 0######################################################
                   player.on_ground = False###############################################3
                   if(player.on_enemy == False): ###################
                       sprite.healthBar.health += DAMAGE_GRAVITY#########################  
                       player.on_enemy = True ##############################

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
            self.player.sprite.on_enemy = False#######################################################
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)
            
    def check_fire(self):
        if self.player.sprite.manaBar.mana + mana_to_power < 0 :
            self.player.sprite.fire = False
        else:
            if self.player.sprite.fire == True:
                ball_image = pygame.image.load('../graphics/character/fire/ball.png').convert_alpha()
                #print(self.player.sprite.facing_right)
                if self.player.sprite.facing_right == True:
                    ball_sprite = Bullet(self.player.sprite.rect.midright, ball_image, 10)
                else: ball_sprite = Bullet(self.player.sprite.rect.midleft, ball_image, -10)
                self.ball.add(ball_sprite)
                self.player.sprite.manaBar.mana += mana_to_power 
                self.player.sprite.fire = False
            

    def run(self):
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        
#       self.checkEndgame()########################################      
#       self.barrier_sprites.draw(self.display_surface)###################################
#       self.barrier_sprites.update(self.world_shift)#############################
        
        #coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        
        #enemy
        self.enemy_sprites.update(self.world_shift)###############################################
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reserse()
        self.enemy_sprites.draw(self.display_surface)
        
        self.box_collision()########################################
        self.box_sprites.update(self.world_shift)#######################################
        self.box_sprites.draw(self.display_surface)###################################
        
        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)
        
        #player sprites
        self.player.update()
        
        self.scroll_x()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.get_player_on_ground()
        self.create_landing_dust()
        
        self.check_fire()
        
        self.ball.update()
        self.ball.draw(self.display_surface)
        
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
    
        
        #health&mana bar
        self.player.sprite.healthBar.draw(self.display_surface,self.player.sprite.rect,'player')################################################
        self.player.sprite.manaBar.draw(self.display_surface,self.player.sprite.rect)################################################
        for enemy in self.enemy_sprites :##################################################
            enemy.healthBar.draw(self.display_surface,enemy.rect,'enemy')
            
           
      