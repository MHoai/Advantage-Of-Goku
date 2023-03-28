import pygame, sys
from settings import screen_width,screen_height
def endGame(type):
    screen = pygame.display.set_mode((screen_width,screen_height))
    if(type == 'win'):
        start_game_bg =pygame.image.load('../endGameImage/end_1.png')
    else :
        start_game_bg =pygame.image.load('../endGameImage/end_2.png')
    start_game_rect = start_game_bg.get_rect()


    while True :
        screen.blit(start_game_bg,start_game_rect)
        for event in pygame.event.get():
             #Check to see if the user wants to quit
            if event.type == pygame.QUIT:
                #End the game
                pygame.quit() 
                sys.exit()
            
        pygame.display.update()