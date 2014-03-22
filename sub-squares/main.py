#!/usr/bin/env python2

#################################################
#TO DO:
#   seperate level and platforms into their own module,
#  it really needs to be cleaned up.
#                   work out what could be its own module and
#               what other classes they depend on.. this could be very circular
#
#  transform player's image based on direction (flip if left or right)
#
#    change the paths so they don't care if it's unix-like or windows
#
#      Some kind of Enemy(s) must be made
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

    player = Player((300,300))
    level_list = [Level01(), Level02()]

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(player)
                #start bullet from the correct side of the player
                if player.facing == 'right':
                    bullet.rect.x = player.rect.right
                else:
                    bullet.rect.x = player.rect.left
                bullet.rect.y = player.rect.y + player.rect.height / 2  #       here
                #current_level.all_sprites_list.add(bullet)
                current_level.bullet_list.add(bullet)


        active_sprite_list.update()

        current_level.update()

        #if player.rect.right > SCREENW:
            #player.rect.right = SCREENW

        #if player.rect.left < 0:
            #player.rect.left = 0

        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)

        if player.rect.x <= 120:
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.shift_world(diff)

        #current position is the player position relative to the screen offset by the amount the world is shifted by
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit_r: #if current position is less than the level limit
            if player.rect.x == 500: #prevents that annoying math issue that was causing it to switch when you retraced your steps
                player.rect.x = 120#put player at left side
                if current_level_no < len(level_list) - 1:#if there's another level in the list after this one
                    current_level_no += 1              # increment current level counter
                    current_level = level_list[current_level_no] #and switch to it
                    player.level = current_level #update player.level property

        if current_position > current_level.level_limit_l:
            if player.rect.y <= 125:
                player.rect.x = 500
                if level_list.pop():
                    current_level_no -= 1
                    current_level = level_list[current_level_no]
                    player.level = current_level

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

        current_level.draw()  #call draw function from current level
        active_sprite_list.draw(SCREEN) #if you call a pygame.sprite.Group.draw() method you must pass it the surface to draw to

        CLOCK.tick(30)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()












