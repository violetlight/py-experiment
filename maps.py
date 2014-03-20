import pygame


class Landscape(object):

    def __init__(self): pass

TILESET = pygame.image.load('images/tiles.png')

g = pygame.Rect(0,0,  32,32)
e = pygame.Rect(0,32, 32,32)
s = pygame.Rect(32,32, 32,32)
d = pygame.Rect(0,64, 32,32)


MAP =  [[s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g],
        [e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
        [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d]]

