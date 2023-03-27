import pygame, sys
from about import *
def startGame(screen):
    startGame = True
    start_game_bg_1 =pygame.image.load('../startGameImage/start_1.png')
    start_game_rect = start_game_bg_1.get_rect()

    start_game_bg_2 =pygame.image.load('../startGameImage/start_2.png')
    #rectangle bound around play button
    buttonRect = pygame.Rect(525, 450, 217, 188)
    buttonAboutRect = pygame.Rect(1024, 68, 215, 52)
    
    pygame.mixer.music.load("../music/start_music.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0)
    
    inButton = 0
    while startGame :
        if not inButton :
            screen.blit(start_game_bg_1,start_game_rect)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
           #Check to see if player move the mouse
            if event.type == pygame.MOUSEMOTION:
                if buttonRect.collidepoint(mouse_x, mouse_y) :
                    inButton = 1
                    screen.blit(start_game_bg_2,start_game_rect)
                else :
                    inButton = 0
             #Check player right click
            if event.type == pygame.MOUSEBUTTONUP:
                if buttonRect.collidepoint(mouse_x, mouse_y) :
                    startGame = False
                    break
                elif buttonAboutRect.collidepoint(mouse_x, mouse_y):
                    aboutGame(screen)
             #Check to see if the user wants to quit
            if event.type == pygame.QUIT:
                #End the game
                pygame.quit() 
                sys.exit()
        pygame.display.update()
    pygame.mixer.music.stop()