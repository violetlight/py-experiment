import pygame

pygame.init()
#######################################
#                                     #
#        GAME SETTINGS                #
#                                     #
#######################################

CLOCK = pygame.time.Clock()

### TIME AND SPEED ###
FPS = 60
PLAYERSPEED = 4
BULLETSPEED = 20

### SIZES ###
SCREENSIZE = SCREENW, SCREENH = 800, 664
GAMESURFSIZE = GAMESURFW, GAMESURFH = 800, 600
STATSURFSIZE = STATSURFW, STATSURFH = 800, SCREENH-GAMESURFH
PLAYERSIZE = PLAYERW, PLAYERH = 32, 96
BULLETSIZE = (10, 4)
PLATFORMH = 32

### SCREENS AND SURFACES ###
SCREEN = pygame.display.set_mode(SCREENSIZE)
GAMESURFACE = pygame.Surface(GAMESURFSIZE)
GAMESURFRECT = GAMESURFACE.get_rect()
STATSURFACE = pygame.Surface(STATSURFSIZE)
STATSURFRECT = STATSURFACE.get_rect(top=GAMESURFH)

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

BULLETCOLOR = ( 216,  218,  214)
WALLCOLOR  =  ( 109, 94,  94)

