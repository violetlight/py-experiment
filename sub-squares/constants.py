import pygame

pygame.init()
#######################################
#
#        GAME SETTINGS
#
#######################################

CLOCK = pygame.time.Clock()
SCREENSIZE = SCREENW, SCREENH = 800, 600
SCREEN = pygame.display.set_mode(SCREENSIZE)
PLAYERSIZE = PLAYERW, PLAYERH = 32, 96
BULLETSPEED = 20
BULLETSIZE = (10, 4)

#######################################
#
#        COLORS
#
#######################################

BLACK = ( 35, 35,  35)
WHITE = (235, 235, 235)
RED   = (255,  64,  64)
BLUE  = ( 64,  64, 255)
GREEN = ( 64, 255,  64)

BULLETCOLOR = ( 16,  18,  14)
WALLCOLOR  =  ( 74, 109,  92)

