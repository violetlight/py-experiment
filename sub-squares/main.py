#!/usr/bin/env python2
import pygame
import sys
from random import randint
from constants import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(WALLCOLOR)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Player(pygame.sprite.Sprite):

    change_x = 0
    change_y = 0
    level = None

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(PLAYERSIZE)
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):
        ###move player###
        #gravity
        self.calc_grav()
        #left/right
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        #up/down
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= SCREENH - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREENH - self.rect.height

    def jump(self):

        #moves down two px to check for platform collision below
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        #if collided with a platform or if you're at the bottom of the screen
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10 #jump

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
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

class Level(object):
    platform_list = None
    enemy_list = None

    background = None

    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        screen.fill(WHITE)

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

class Level01(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        level = [[210, 70, 500, 500],
                [210, 70, 200, 400],
                [210, 70, 600, 300],
                ]
        for platform in level:
            block = Platform((platform[0], platform[1]))
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


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
                if event.key == pygame.K_UP:
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












