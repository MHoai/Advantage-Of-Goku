import pygame, sys

def aboutGame(screen):
    aboutGame = True
    about_game_bg =pygame.image.load('../startGameImage/about.png')
    about_game_rect = about_game_bg.get_rect()

    #rectangle bound around play button
    buttonRect = pygame.Rect(1024, 645, 117, 128)
    
    while aboutGame :
        screen.blit(about_game_bg,about_game_rect)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():

             #Check player right click
            if event.type == pygame.MOUSEBUTTONUP:
                if buttonRect.collidepoint(mouse_x, mouse_y) :
                    aboutGame = False
                    break
             #Check to see if the user wants to quit
            if event.type == pygame.QUIT:
                #End the game
                pygame.quit() 
                sys.exit()
        pygame.display.update()