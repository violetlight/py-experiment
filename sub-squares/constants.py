import pygame

pygame.init()
#######################################
#                                     #
#        GAME SETTINGS                #
#                                     #
#######################################

CLOCK = pygame.time.Clock()
FPS = 60
SCREENSIZE = SCREENW, SCREENH = 800, 600
SCREEN = pygame.display.set_mode(SCREENSIZE)
SCREENRECT = SCREEN.get_rect()
PLAYERSIZE = PLAYERW, PLAYERH = 32, 96
BULLETSPEED = 20
BULLETSIZE = (10, 4)
PLATFORMH = 32

#######################################
#                                     #
#        COLORS                       #
#                                     #
#######################################

BLACK  = ( 35, 35,  35)
WHITE  = (235, 235, 235)
RED    = (255,  64,  64)
BLUE   = ( 64,  64, 255)
GREEN  = ( 64, 255,  64)
YELLOW = (227, 215,  50) 

BULLETCOLOR = ( 16,  18,  14)
WALLCOLOR  =  ( 74, 109,  92)

