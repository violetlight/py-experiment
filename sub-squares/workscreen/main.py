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

class Circe(pygame.sprite.Sprite):
    image = pygame.Surface((100,100))
    image.set_colorkey((3,0,0))
    pygame.draw.circle(image, (255,0,0), (50,50), 50, 2)
    image.convert_alpha()


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Circe.image
        self.rect = self.image.get_rect()
        self.radius = 50
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
sprites = pygame.sprite.Group()
c = Circe()
sprites.add(c)
while 1:
    screen.fill((240,240,240))

    sprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
