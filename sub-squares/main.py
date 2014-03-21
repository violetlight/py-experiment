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

        self.facing = 'right'
        self.effects = []

        #At 1, this is essentially inactive. to slow, lower than 1, to speed up, higher than 1
        self.speedmodifier = 1

        #default gravity amount
        self.grav_amount = .35

    def update(self):
        ###move player###
        #gravity
        self.calc_grav(self.grav_amount)
        #left/right
        self.rect.x += self.change_x

        ###check for collision with gravity_blocks###
        block_hit_list = pygame.sprite.spritecollide(self, self.level.special_blocks, False)
        for block in block_hit_list:

            ###Gravity Powerup Block###
            if isinstance(block, GravityBlock):
                self.grav_start = time() #Start timer for effect
                self.grav_amount = .15   #Status effected
                self.effects.append('low_gravity') #Append to effects list
                self.level.special_blocks.remove(block) #Remove the block you got

            ###Speed Powerup Block###
            if isinstance(block, SpeedBlock):
                self.speed_start = time() #Start timer for effect
                self.speedmodifier = 2    #Status affected
                self.effects.append('speed') #Append to effects list
                self.level.special_blocks.remove(block) #Remove the block you got

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


        ###check for status effects###
        if self.effects:
            for effect in self.effects:
                if effect == 'speed':
                    if time() - self.speed_start > 5: #checks for five seconds since the effect started, if it has been longer than 5 seconds...
                        self.speedmodifier = 1  #reset speed
                        self.effects.remove(effect)     #remove effect

                if effect == 'low_gravity':          #same model as above..
                    if time() - self.grav_start > 5:
                        self.grav_amount = .35
                        self.effects.remove(effect)

    def calc_grav(self, amount):
        if self.change_y == 0:#if change_y is nothing...
            self.change_y = 1 #keep pushing player down one...?
        else:
            self.change_y += amount #otherwise, if change_y is anything, add .35 to it (positive numbers represent downward motion)

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
        self.change_x = -6 * self.speedmodifier
        if self.facing == 'right':
            self.image = pygame.transform.flip(self.image, 1, 0) #flips image based on direction
            self.facing = 'left'

    def go_right(self):
        self.change_x = 6 * self.speedmodifier
        if self.facing == 'left':
            self.image = pygame.transform.flip(self.image, 1, 0) #same thing as above
            self.facing = 'right'

    def stop(self):
        self.change_x = 0

    def stopjump(self):
        self.change_y = self.change_y / 2 #contols the way the jump handles when you release space bar

class Bullet(pygame.sprite.Sprite):
    """A class for Bullet objects"""
    def __init__(self, owner):
        pygame.sprite.Sprite.__init__(self)

        self.owner = owner
        #To get the constant direction of the bullet, get the direction that the person who shot it was facing when they did
        self.direction = self.owner.facing
        self.image = pygame.Surface((4, 10)) #4,10 is the size
        self.image.fill(BULLETCOLOR) #a blackish color
        self.rect = self.image.get_rect()

    def update(self): #moves bullet in direction
        if self.direction == 'right':
            self.rect.x += BULLETSPEED
        else:
            self.rect.x -= BULLETSPEED


class Platform(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(WALLCOLOR)

        self.rect = self.image.get_rect()

class GravityBlock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((32,32))
        self.blue = 100 # used in color fading
        self.blueup = True # used for direction in color fading
        self.image.fill((20, 45, self.blue))
        self.rect = self.image.get_rect()

    def update(self):
        """Fades color brightness in and out"""
        if self.blueup:
            self.blue += 8
            if self.blue >= 245:
                self.blueup = False
        else:
            self.blue -= 8
            if self.blue <= 100:
                self.blueup = True

        self.image.fill((10, 25, self.blue))

class SpeedBlock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((32,32))
        self.green = 100
        self.greenup = True
        self.image.fill((180, self.green, 20))
        self.rect = self.image.get_rect()

    def update(self):
        if self.greenup:
            self.green += 8
            if self.green >= 245:
                self.greenup = False
        else:
            self.green -= 8
            if self.green <= 100:
                self.greenup = True

        self.image.fill((180, self.green, 20))

class Level(object):
    platform_list = None
    enemy_list = None
    special_blocks = None

    background = None
    world_shift = 0

    def __init__(self, player):

        self.platform_list = pygame.sprite.Group() #group for platforms
        self.enemy_list = pygame.sprite.Group() # group for enemies.. not yet used
        self.special_blocks = pygame.sprite.Group() #group for gravity blocks
        self.bullet_list = pygame.sprite.Group()
        #self.all_sprites_list = pygame.sprite.Group()
        self.player = player # player passed to level

    def update(self):
        self.platform_list.update() #call update on every platform object
        self.enemy_list.update() # and every enemy object ... not yet used though--so empty
        self.special_blocks.update() #update special blocks
        self.bullet_list.update() #might be able to remove all of these
        #self.all_sprites_list.update()

    def shift_world(self, shift_x):
        self.world_shift += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
        for block in self.special_blocks:
            block.rect.x += shift_x

class Level01(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -1000

        level = [[210, 70, 500, 500],  #a list of platform rect-style  lists
                [210, 70, 200, 400],
                [210, 70, 600, 300],
                [210, 70, 100, 100],
                [420, 70, 1000, SCREENH/2],
                ]
        for platform in level:  #for each element of level, create a platform
            block = Platform((platform[0], platform[1]))
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block) #and add it to platform list

        #Create gravity block and add it to the special_blocks list
        gravityblock = GravityBlock()
        gravityblock.rect.x = 200
        gravityblock.rect.y = 336
        gravityblock.player = self.player

        speedblock = SpeedBlock()
        speedblock.rect.x = 600
        speedblock.rect.y = 250
        speedblock.player = self.player
        self.special_blocks.add(gravityblock, speedblock)
        #self.all_sprites_list.add(gravityblock, speedblock)

    def draw(self):

        SCREEN.fill(WHITE)
        self.platform_list.draw(SCREEN)
        self.enemy_list.draw(SCREEN)
        self.special_blocks.draw(SCREEN)
        self.bullet_list.draw(SCREEN)
        #self.all_sprites_list.draw(SCREEN)

class Level02(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -1000

        level = [[110, 70, 520, 400],  #a list of platform rect-style  lists
                [110, 70, 200, 400],
                [110, 70, 600, 300],
                [110, 70, 100, 100],
                [120, 70, 1000, SCREENH/2],
                ]
        for platform in level:  #for each element of level, create a platform
            block = Platform((platform[0], platform[1]))
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block) #and add it to platform list

        #Create gravity block and add it to the special_blocks list
        gravityblock = GravityBlock()
        gravityblock.rect.x = 250
        gravityblock.rect.y = 336
        gravityblock.player = self.player

        #creates a speed powerup block and adds it to the list
        speedblock = SpeedBlock()
        speedblock.rect.x = 600
        speedblock.rect.y = 250
        speedblock.player = self.player
        self.special_blocks.add(gravityblock, speedblock)

        #self.all_sprites_list.add(gravityblock, speedblock)

    def draw(self):

        SCREEN.fill(GREEN)
        self.platform_list.draw(SCREEN)
        self.enemy_list.draw(SCREEN)
        self.special_blocks.draw(SCREEN)
        #self.all_sprites_list.draw(SCREEN)



def main():
    #pygame.init()

    player = Player((300,300))
    level_list = [Level01(player), Level02(player)]

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
                bullet.rect.x = player.rect.right     #adjust bullet origin
                bullet.rect.y = player.rect.y + player.rect.height / 2  #       here
                #current_level.all_sprites_list.add(bullet)
                current_level.bullet_list.add(bullet)


        active_sprite_list.update()

        current_level.update()

        if player.rect.right > SCREENW:
            player.rect.right = SCREENW

        if player.rect.left < 0:
            player.rect.left = 0

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
        if current_position < current_level.level_limit: #if current position is less than the level limit
            player.rect.x = 120#put player at left side
            if current_level_no < len(level_list) - 1:#if there's another level in the list after this one
                current_level_no += 1              # increment current level counter
                current_level = level_list[current_level_no] #and switch to it
                player.level = current_level #update player.level property

        for bullet in current_level.bullet_list: #iterate over the bullets (which are kept track of in the level... maybe that will change)
            block_hit_list = pygame.sprite.spritecollide(bullet, current_level.enemy_list, False) #see if it collided with an enemy (none yet)
            for block in block_hit_list:#if it did, remove the bullet
                current_level.bullet_list.remove(bullet)
            if bullet.rect.x < 0 or bullet.rect.x > SCREENW: #if it goes offscreen
                current_level.bullet_list.remove(bullet)  #    remove       it


        current_level.draw()  #call draw function from current level
        active_sprite_list.draw(SCREEN) #if you call a pygame.sprite.Group.draw() method you must pass it the surface to draw to

        CLOCK.tick(30)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()












