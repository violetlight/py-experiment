#!/usr/bin/env python2

#################################################
#TO DO:                                         #
#                                               #
#                                               #
#                                               #
#   change the paths so they don't care if it's #
#    unix-like or windows.                      #
#                                               #
#      Some kind of Enemy(s) must be made       #
#                                               #
#   Resize screen and make room for a status    #
#      bar of some kind to display game stats   #
#                                               #
#################################################

from __future__ import print_function
import pygame
import sys
from time import time
from random import randint
from constants import *
from player import Player, Bullet
from levels import *


#######################################
#                                     #
#   Main Loop                         #
#                                     #
#######################################
def main():
    #pygame.init()

    player = Player((300,300))#starting position of the player
    #level_list = [Level01(), Level02()]

    #current level number
    current_level_no = 0
    current_level = mainlist["starting"]       #level_list[current_level_no]
    #point this to levels.mainlist["starting"] or something


    background = pygame.Surface(SCREEN.get_size()).convert()
    background.fill(WHITE)

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    active_sprite_list.add(player)

    done = False

    while not done:


        ##########################
        #   Event loop           #
        ##########################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            #call player methods based on keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_SPACE:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()
                if event.key == pygame.K_SPACE and player.change_y < 0:
                    player.stopjump() # if player releases space it calls stopjump, player can control jump amount

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bullet = Bullet(player)
                #start bullet from the correct side of the player
                if player.facing == 'right':
                    bullet.rect.x = player.rect.right
                else:
                    bullet.rect.x = player.rect.left
                bullet.rect.y = player.rect.y + player.rect.height / 2  #       here
                #current_level.all_sprites_list.add(bullet)
                current_level.bullet_list.add(bullet)


        ##########################
        #  Call updates          #
        ##########################
        active_sprite_list.update() #investigate this..
        current_level.update()


        ##########################
        #  World shifting        #
        ##########################
        current_position = player.rect.x + current_level.world_shift

        ### RIGHT SIDE ###
        if current_position > current_level.level_limit_r and player.shiftingr:
            if player.rect.x >= 500:
                diff = player.rect.x - 500
                player.rect.x = 500
                current_level.shift_world(-diff)
        elif current_position <= current_level.level_limit_r:
            player.shiftingr = False
        elif player.shiftingr == False:
            if player.rect.right > SCREENW:
                player.rect.right = SCREENW
            if player.rect.x <= 120:
                player.shiftingr = True

        ### LEFT SIDE ###
        if current_position < current_level.level_limit_l and player.shiftingl:
            if player.rect.x <= 120:
                diff = 120 - player.rect.x
                player.rect.x = 120
                current_level.shift_world(diff)
        elif current_position >= current_level.level_limit_l:
            player.shiftingl = False
        elif player.shiftingl == False:
            if player.rect.x < 0:
                player.rect.x = 0
            if player.rect.x >= 500:
                player.shiftingl = True

        #########################
        #  D E B U G            #
        #########################
        #print("Current position", current_position)
        #print("Left level limit", current_level.level_limit_l)
        #print("Right level limit", current_level.level_limit_r)
        #print("World shift", current_level.world_shift)


        ##########################
        #  Bullet collision      #
        ##########################

        for bullet in current_level.bullet_list: #iterate over the bullets (which are kept track of in the level... maybe that will change)

            ###check for collision with ENEMY###
            block_hit_list = pygame.sprite.spritecollide(bullet, current_level.enemy_list, False) #see if it collided with an enemy (none yet)
            for block in block_hit_list:#if it did, remove the bullet
                current_level.bullet_list.remove(bullet)
            if bullet.rect.x < 0 or bullet.rect.x > SCREENW: #if it goes offscreen
                current_level.bullet_list.remove(bullet)  #    remove       it

            ###Check for collision with Platforms###
            block_hit_list = pygame.sprite.spritecollide(bullet, current_level.platform_list, False)
            for block in block_hit_list:
                current_level.bullet_list.remove(bullet)


        #########################
        #  Call draw methods    #
        #########################

        current_level.draw()  #call draw function from current level
        active_sprite_list.draw(SCREEN) #if you call a pygame.sprite.Group.draw() method you must pass it the surface to draw to


        if current_level != player.level:
            current_level = player.level

        CLOCK.tick(FPS)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()












