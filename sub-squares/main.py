#!/usr/bin/env python2

#################################################
#TO DO:
#   seperate level and platforms into their own module, 
#  it really needs to be cleaned up. 
#
#  transform player's image based on direction (flip if left or right)
#



import pygame
import sys
from random import randint
from constants import *

class Player(pygame.sprite.Sprite):

    #initialize these variables
    change_x = 0
    change_y = 0
    level = None

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)


        #player image
        self.image = pygame.image.load('../images/trent.png')
        #self.image = pygame.Surface(PLAYERSIZE)
        #self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        ###move player###
        #gravity
        self.calc_grav()
        #left/right
        self.rect.x += self.change_x

        ###check for collisions with platforms###
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0: #if moving right
                self.rect.right = block.rect.left #set the right edge of the player to the left edge fo the block you collided with
            elif self.change_x < 0: #if moving left
                self.rect.left = block.rect.right #do the inverse

        #up/down, player's y position changes based on value of self.change_y
        self.rect.y += self.change_y

        ###check for collisions with platforms again... why?###
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:#if moving down
                self.rect.bottom = block.rect.top #set the bottom of the player rect to the top of the block you collided with
            elif self.change_y < 0:#if moving up
                self.rect.top = block.rect.bottom#do the inverse

            self.change_y = 0 #reset self.change_y value so that you aren't moving up anymore if jumping and gravity can take its course


    def calc_grav(self):
        if self.change_y == 0:#if change_y is nothing...
            self.change_y = 1 #keep pushing player down one...?
        else:
            self.change_y += .35 #otherwise, if change_y is anything, add .35 to it (positive numbers represent downward motion)

        #if bottom of player is outside of screen and still moving down...
        if self.rect.y >= SCREENH - self.rect.height and self.change_y >= 0:
            self.change_y = 0 #stop y motion
            self.rect.y = SCREENH - self.rect.height #set player's bottom edge on bottom of screen

    def jump(self):

        #moves down two px to check for platform collision below
        self.rect.y += 2
        #should collide if platform is below
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2 #moves back up

        #if collided with a platform or if you're at the bottom of the screen, then you are allowed to jump
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREENH:
            self.change_y = -10 #jump.. negative

    #player controlled movement
    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(WALLCOLOR)

        self.rect = self.image.get_rect()

class Level(object):
    platform_list = None
    enemy_list = None

    background = None

    def __init__(self, player):

        self.platform_list = pygame.sprite.Group() #group for platforms
        self.enemy_list = pygame.sprite.Group() # group for enemies.. not yet used
        self.player = player # player passed to level

    def update(self):
        self.platform_list.update() #call update on every platform object
        self.enemy_list.update() # and every enemy object ... not yet used though--so empty

    def draw(self, screen):
        screen.fill(WHITE)

        self.platform_list.draw(screen) #draw every platform based on their image and rect
        self.enemy_list.draw(screen) #   and enemies if they existed

class Level01(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        level = [[210, 70, 500, 500],  #a list of platform rect-style  lists
                [210, 70, 200, 400],
                [210, 70, 600, 300],
                [210, 70, 100, 100],
                ]
        for platform in level:  #for each element of level, create a platform
            block = Platform((platform[0], platform[1]))
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block) #and add it to platform list


def main():
    #pygame.init()

    player = Player((300,300))
    level_list = []
    level_list.append(Level01(player))

    #current level number
    current_level_no = 0
    current_level = level_list[current_level_no]

    background = pygame.Surface(SCREEN.get_size()).convert()
    background.fill(WHITE)

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    active_sprite_list.add(player)

    done = False

    while not done:
        SCREEN.blit(background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_SPACE:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        active_sprite_list.update()

        current_level.update()

        if player.rect.right > SCREENW:
            player.rect.right = SCREENW

        if player.rect.left < 0:
            player.rect.left = 0

        current_level.draw(SCREEN)
        active_sprite_list.draw(SCREEN)

        CLOCK.tick(30)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()












