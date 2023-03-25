import pygame, sys
from settings import * 
from level import Level
from game_data import level_0
from start import * ###########################
# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_0,screen)
#start game
startGame(screen)##############################################s

# main loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill('grey')
	level.run()#########################

	pygame.display.update()
	clock.tick(60)