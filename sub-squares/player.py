from __future__ import print_function
from constants import *
import pygame
from levels import GravityBlock, SpeedBlock, DoorBlock, mainlist #This will hopefully be changed so that it doesn't need to do this
from time import time

#######################################
#                                     #
#     Player                          #
#                                     #
#######################################
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
        self.shiftingr = True
        self.shiftingl = True

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

        ######################################
        #  Power Up/Event Block Collision    #
        ######################################
        block_hit_list = pygame.sprite.spritecollide(self, self.level.special_blocks, False)
        for block in block_hit_list:

            ###GRAVITY###
            if isinstance(block, GravityBlock):
                self.grav_start = time() #Start timer for effect
                self.grav_amount = .15   #Status effected
                self.effects.append('low_gravity') #Append to effects list
                self.level.special_blocks.remove(block) #Remove the block you got

            ###SPEED UP###
            if isinstance(block, SpeedBlock):
                self.speed_start = time() #Start timer for effect
                self.speedmodifier = 2    #Status affected
                self.effects.append('speed') #Append to effects list
                self.level.special_blocks.remove(block) #Remove the block you got

            ###DOOR###
            if isinstance(block, DoorBlock):
                if block.cooldown == "off":
                    if pygame.key.get_pressed()[pygame.K_w] or block.auto:
                        self.rect.bottomleft = mainlist[block.room].doorlist[block.linkeddoor].rect.bottomleft
                        mainlist[block.room].doorlist[block.linkeddoor].cooldown = "on"
                        self.level = mainlist[block.room]


        ###############################
        #   Platform Collision        #
        ###############################
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
        if self.rect.y >= GAMESURFH - self.rect.height and self.change_y >= 0:
            self.change_y = 0 #stop y motion
            self.rect.y = GAMESURFH - self.rect.height #set player's bottom edge on bottom of screen

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

#######################################
#                                     #
#    Projectiles                      #
#                                     #
#######################################
class Bullet(pygame.sprite.Sprite):
    """A class for Bullet objects"""
    def __init__(self, owner):
        pygame.sprite.Sprite.__init__(self)

        self.owner = owner
        #To get the constant direction of the bullet, get the direction that the person who shot it was facing when they did
        self.direction = self.owner.facing
        self.image = pygame.Surface(BULLETSIZE) #4,10 is the size
        self.image.fill(BULLETCOLOR) #a blackish color
        self.rect = self.image.get_rect()

    def update(self): #moves bullet in direction
        if self.direction == 'right':
            self.rect.x += BULLETSPEED
        else:
            self.rect.x -= BULLETSPEED

