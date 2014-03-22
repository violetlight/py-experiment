#!/usr/bin/env python2


###########################################
#                                         #
# This is a super simple environment to   #
# use in testing of basic pygame behav-   #
# ior.                                    #
#                                         #
###########################################

import pygame, sys

pygame.init()
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()


while 1:
    screen.fill((240,240,240))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
