import pygame
from support import import_csv_layout, import_cut_graphic
from settings import *
from tile import Tile, StaticTile, AnimatedTile, Coin
from enemy import Enemy
from player import Player
from particles import ParticleEffect
from bullet import Bullet
from boss import Boss
from box import *#######################
from end import *##############################
from super_box import *##########################

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift_x = 0
        self.world_shift_y = 0
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
        
        
        #enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')    
        #constraint    
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')   
        
        #boss setup
        boss_layout = import_csv_layout(level_data['boss'])
        self.boss_sprite = self.create_tile_group(boss_layout, 'boss') 
        
        #box 
        box_layout = import_csv_layout(level_data['boxs'])
        self.box_sprites = self.create_tile_group(box_layout, 'boxs') 
        
        #barrier
        barrier_layout = import_csv_layout(level_data['barriers'])
        self.barrier_sprites = self.create_tile_group(barrier_layout, 'barriers') 

        #thorn
        thorn_layout = import_csv_layout(level_data['thorns'])
        self.thorn_sprites = self.create_tile_group(thorn_layout, 'thorns') 
        
        #super_box
        super_box_layout = import_csv_layout(level_data['super_box'])
        self.super_box_sprites = self.create_tile_group(super_box_layout, 'super_box') 
        
        #key
        key_layout = import_csv_layout(level_data['key'])
        self.key_sprites = self.create_tile_group(key_layout, 'key') 
        
        #coins
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins') 
        
    
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('../graphics/terrain/Assets.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)####################################
                    elif type == 'coins':
                        sprite = Coin(tile_size,x,y,'../graphics/coins/gold')
                        sprite_group.add(sprite)#############################
                    elif type == 'enemies':
                        sprite = Enemy(tile_size, x, y)
                        sprite_group.add(sprite)################################
                    elif type == 'boxs':########################
                         sprite = Box_Animated(tile_size, x, y)###########################
                         sprite_group.add(sprite)#########################
                    elif type == 'constraints':
                        sprite = Tile(tile_size, x, y)     
                        sprite_group.add(sprite)########################
                    elif type == 'boss':
                        sprite = Boss(x,y) 
                        sprite_group.add(sprite)####################
                    elif type == 'super_box':########################
                         sprite = Super_Box_Animated(tile_size, x, y)#######################
                         sprite_group.add(sprite)#################################
                          
                    elif type == 'barriers':##################################
                        terrain_tile_source = import_cut_graphic('../graphics/terrain/Assets.png')################
                        tile_surface = terrain_tile_source[int(val)]########################
                        sprite = StaticTile(tile_size, x, y, tile_surface)  ####################   
                        sprite_group.add(sprite)  ##############################    
                    elif type == 'thorns':##################################
                        terrain_tile_source = import_cut_graphic('../graphics/terrain/Assets.png')#######################
                        tile_surface = terrain_tile_source[int(val)]#######################
                        sprite = StaticTile(tile_size, x, y, tile_surface)######################
                        sprite_group.add(sprite)
                    elif type == 'key':#####################
                        sprite = Coin(tile_size,x,y,'../graphics/key')###################
                        
                        sprite_group.add(sprite)  ##############################  
                        
        return sprite_group
    
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val != '-1':
                    sprite = Player((x,y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
     #           if val == '1':
      #              hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
       #             sprite = StaticTile(tile_size, x, y, hat_surface)
       #             self.goal.add(sprite)
                    
    
    def enemy_collision_reserse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()
                
        for boss in self.boss_sprite.sprites():
            if pygame.sprite.spritecollide(boss, self.constraint_sprites, False):
                boss.speed = 0
    
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
    def coin_collision(self):
        player = self.player.sprite################################################
        collidable_sprites = self.coins_sprites.sprites()###############################################
        for sprite in collidable_sprites: #################################
                if sprite.rect.colliderect(player):#############################
                    if player.collect_coin:
                      player.healthBar.health += coin_add_hp
                      if player.healthBar.health>100: player.healthBar.health = 100
                      player.collect_coin = False
                      sprite.kill()
                else:  player.collect_coin = True
                
    def barriers_collision(self):####################################
        player = self.player.sprite################################################
        collidable_sprites = self.barrier_sprites.sprites()###############################################
        if(player.killed_boss):#############################
           for sprite in collidable_sprites: #################################
                if sprite.rect.colliderect(player):############################# 
                      sprite.rect.x += 1#################################  
        else:
            for sprite in collidable_sprites: #################################
                if sprite.rect.colliderect(player):############################# 
                    player.rect.right = sprite.rect.left#############################
                    player.on_right = True########################################
                    self.current_x = player.rect.right####################################
            if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
                player.on_right = False
    
    def key_collision(self):####################
         player = self.player.sprite################################################
         collidable_sprites = self.key_sprites.sprites()###############################################
         for sprite in collidable_sprites: #################################
                if sprite.rect.colliderect(player):#############################
                    player.healthBar.health = -9999 ############
                    sprite.kill()############################
    
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
                         elif(sprite.gift == 2) : ####################################33
                            if player.manaBar.mana + addMana <= 100 :#########################
                                player.manaBar.mana += addMana################################################
                            else: player.manaBar.mana = 100#################################   
                     if sprite.pass_time :#########################################################
                         if pygame.time.get_ticks()-sprite.pass_time>=1000 :###############################
                            sprite.kill()############################################     
                            player.canmove = True 
    
    def super_box_collision(self):#########################################
         player = self.player.sprite################################################
         collidable_sprites = self.super_box_sprites.sprites()###############################################
         for sprite in collidable_sprites: #################################
                if sprite.rect.colliderect(player):#############################
                     player.canmove = False
                     sprite.be_hited = True###################################
                     if sprite.pass_time == 0 :## chi cap nhat gift cho lan dau tien#######################################################
                         sprite.pass_time = pygame.time.get_ticks() #######################
                         player.ssj = True  
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
               # if player.direction.y==0:##############################
                    if player.direction.x < 0 and  (player.rect.bottomleft[1] < sprite.rect.topleft[1]):################# 
                        player.rect.left = sprite.rect.right
                        player.on_left = True
                        self.current_x = player.rect.left
                    elif player.direction.x > 0 and (player.rect.bottomleft[1] < sprite.rect.topleft[1]):####################
                        player.rect.right = sprite.rect.left
                        player.on_right = True
                        self.current_x = player.rect.right
             #   elif player.direction.y>0:########################
             #       if player.direction.x < 0 : ##########################
             #           player.rect.left = sprite.rect.right#######################
              #          player.on_left = True###########################
             #           self.current_x = player.rect.left##########################
             #       elif player.direction.x > 0 :######################
             #           player.rect.right = sprite.rect.left#############################
              #          player.on_right = True#############################
              #          self.current_x = player.rect.right##########################################
        for sprite in collidable_enemy: ##########################################
            for ball in self.ball:####################################
                if sprite.rect.colliderect(ball):##################
                    if(player.ssj):
                       sprite.healthBar.health += SSJ_DAMAGE_POWER ################################# 
                    else:
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
                if(player.status=='hit') and (not player.on_enemy):#####################
                    if(sprite.be_hited):####################
                        if(player.ssj):###############################################
                            sprite.healthBar.health +=SSJ_DAMAGE_HIT####################
                        else: sprite.healthBar.health +=DAMAGE_HIT####################
                        if(player.mana+hit_to_add_mana<=100): player.mana += hit_to_add_mana
                        sprite.be_hited = False#############################
                else:##########################
                    if(player.be_bited) and (not player.on_enemy):####################
                        player.healthBar.health +=DAMAGE_BITE #########################################
                        player.be_bited = False####################
                        player.canmove = False######################################
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
        collidable_thorn = self.thorn_sprites.sprites()##################################
        
        for sprite in collidable_thorn:##################
            if sprite.rect.colliderect(player.rect):#############################
                player.healthBar.health -= 100
                if player.healthBar.health < 0 : player.healthBar.health = 0####################################
                player.canmove = False ###############################

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect) :
                player.on_enemy = False
                if player.direction.y > 0 :
                    if  player.rect.bottomleft[0] != sprite.rect.bottomright[0] and player.rect.bottomright[0] != sprite.rect.bottomleft[0]: 
                      #project nay khong co 2 vat the co cung width nao
                       player.rect.bottom = sprite.rect.top
                       player.direction.y = 0
                       player.on_ground = True
                elif player.direction.y < 0 :########################
                    if  player.rect.bottomleft[0] != sprite.rect.bottomright[0] and player.rect.bottomright[0] != sprite.rect.bottomleft[0]:
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

        if player_x < screen_width / 3 and direction_x < 0:
            self.world_shift_x = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 3) and direction_x > 0:
            self.world_shift_x = -8
            player.speed = 0
        else:
            self.world_shift_x = 0
            player.speed = 8
            
    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y
        
        keys = pygame.key.get_pressed()
        if not (player.status == 'fall' and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT])):
            if player_y < screen_height / 6:# and player.status == 'idle':#################
                self.world_shift_y = 3##############################
            elif player_y > screen_height - (screen_height / 3) :#
               # and  player.status == 'idle':
               #and (not pygame.sprite.spritecollide(player, self.terrain_sprites, False))
                self.world_shift_y = -10
            else: 
                self.world_shift_y = 0
        else:
            self.world_shift_y = 0

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
                if self.player.sprite.facing_right == True:
                    ball_sprite = Bullet(self.player.sprite.rect.midright, ball_image, BULLET_SPEED)
                else: ball_sprite = Bullet(self.player.sprite.rect.midleft, ball_image, -BULLET_SPEED)
                self.ball.add(ball_sprite)
                self.player.sprite.manaBar.mana += mana_to_power 
                self.player.sprite.fire = False
                self.player.sprite.kame_sound.play()
    
    def focus_management(self):
        player = self.player.sprite
        if player.status == 'focus':
            while player.manaBar.mana and player.healthBar.health<100:########################################
                player.healthBar.health += 1
                player.manaBar.mana -= 1

    def Boss_move_and_attack(self, boss, player):
        player = self.player.sprite
        if boss.rect.centerx - player.rect.centerx > 280 and boss.can_move == True:###############
            boss.facing_right = True
            boss.status = "walk"
            boss.rect.x -= boss.speed
            boss.hiting_player = False
            
        elif boss.rect.centerx - player.rect.centerx < -280 and boss.can_move == True:##############
            boss.status = "walk"
            boss.facing_right = False
            boss.rect.x += boss.speed
            boss.hiting_player = False

        elif boss.rect.colliderect(player.rect) :######################
            boss.status = "cleave"
        else:
            boss.status = "idle"
            boss.hiting_player = False
            
        if boss.hiting_player == True:
            player.healthBar.health += DAMAGE_BOSS ###################################

            
    def isDead(self, boss):
        if boss.healthBar.health <= 0:########################################
            boss.status = "death"
            boss.can_move = False
            self.player.sprite.killed_boss = True
            
    def Boss_take_hit(self, boss, player_rect):
        player = self.player.sprite  
        if player.status == 'hit' and boss.rect.colliderect(player_rect):
            boss.status = 'take hit'
            if(player.ssj):
                boss.healthBar.health -= 0.12
            else: boss.healthBar.health -= 0.15 
            if(boss.time_take_hit == 0): boss.time_take_hit = pygame.time.get_ticks()####################
            elif(pygame.time.get_ticks() - boss.time_take_hit >= 2000) : #######################
                boss.status = 'cleave'################################
                boss.hiting_player = True
                boss.time_take_hit = 0##############################
        for ball in self.ball: 
            if (boss.rect.colliderect(ball)):
                boss.status = 'take hit'
                boss.healthBar.health -= 20
                ball.kill()
                   
    #end boss's behavior
        

    def run(self):
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift_x, self.world_shift_y)
        
        self.thorn_sprites.draw(self.display_surface)##############################
        self.thorn_sprites.update(self.world_shift_x, self.world_shift_y)##################################
        
        #barrier
        self.barriers_collision()    
        self.barrier_sprites.draw(self.display_surface)###################################
        self.barrier_sprites.update(self.world_shift_x,self.world_shift_y)#############################
        
        #coins
        self.coin_collision()####################################
        self.coins_sprites.update(self.world_shift_x, self.world_shift_y)#################################
        self.coins_sprites.draw(self.display_surface)#####################################
        
        #enemy
        self.enemy_sprites.update(self.world_shift_x, self.world_shift_y)###############################################
        self.constraint_sprites.update(self.world_shift_x, self.world_shift_y)
        self.enemy_collision_reserse()
        self.enemy_sprites.draw(self.display_surface)       
        
        self.box_collision()########################################
        self.box_sprites.update(self.world_shift_x, self.world_shift_y)#######################################
        self.box_sprites.draw(self.display_surface)###################################
        
        self.super_box_collision()########################################
        self.super_box_sprites.update(self.world_shift_x, self.world_shift_y)#######################################
        self.super_box_sprites.draw(self.display_surface)###################################
        
        # dust particles
        self.dust_sprite.update(self.world_shift_x)
        self.dust_sprite.draw(self.display_surface)
        
        #key
        self.key_collision()#######################################################
        self.key_sprites.update(self.world_shift_x, self.world_shift_y)######################################
        self.key_sprites.draw(self.display_surface)################################
        
        #player sprites
        self.player.update()
        
        self.scroll_x()
        self.scroll_y()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.get_player_on_ground()
        self.create_landing_dust()
        
        self.check_fire()
        
        #ball
        player = self.player.sprite
        self.ball.update(player)
        self.ball.draw(self.display_surface)
        
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift_x, self.world_shift_y)
        self.goal.draw(self.display_surface)
        
        #boss
        self.boss_sprite.update(self.world_shift_x, self.world_shift_y)
        self.boss_sprite.draw(self.display_surface)
        
        bosses = self.boss_sprite.sprites()
        for boss in bosses:
            self.Boss_move_and_attack(boss, player)
            self.isDead(boss)
            self.Boss_take_hit(boss, player.rect)
        
        #focus management
        self.focus_management()
    
        
        #health&mana bar
        self.player.sprite.healthBar.draw(self.display_surface,self.player.sprite.rect,'player')################################################
        self.player.sprite.manaBar.update()################################################
        self.player.sprite.manaBar.draw(self.display_surface,self.player.sprite.rect)################################################
        
        for boss in self.boss_sprite :
            boss.healthBar.draw(self.display_surface,boss.rect,'boss')
        
        for enemy in self.enemy_sprites :##################################################
            enemy.healthBar.draw(self.display_surface,enemy.rect,'enemy')
            
            
           
      