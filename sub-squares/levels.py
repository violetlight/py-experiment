from __future__ import print_function
from constants import *
import pygame
from time import time

#######################################
#                                     #
#    Platform                         #
#                                     #
#######################################
class Platform(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(WALLCOLOR)

        self.rect = self.image.get_rect()


#######################################
#                                     #
#       Power Up Blocks               #
#                                     #
#######################################
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

#######################################
#                                     #
#     Event Blocks                    #
#                                     #
#######################################

#####DOOR#####
class DoorBlock(pygame.sprite.Sprite):

    # takes pos as a tuple and level is a level object
    def __init__(self, name, pos, room, linkeddoor, visible=True):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.linkeddoor = linkeddoor
        self.room = room
        self.image = pygame.Surface((64, 128))
        self.visible = visible
        self.cooldown = "off"
        if self.visible:
            self.image.fill(YELLOW)
        else:
            self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if self.cooldown == "on":
            self.timestart = time()
            self.cooldown = "cooling"
        elif self.cooldown == "cooling":
            if time() - self.timestart >= 1:
                self.cooldown = "off"



#######################################
#                                     #
#           Level Base Class          #
#                                     #
#######################################
class Level(object):
    platform_list = None
    enemy_list = None
    special_blocks = None

    background = None
    world_shift = 0

    def __init__(self):

        self.platform_list = pygame.sprite.Group() #group for platforms
        self.enemy_list = pygame.sprite.Group() # group for enemies.. not yet used
        self.special_blocks = pygame.sprite.Group() #group for gravity blocks
        self.bullet_list = pygame.sprite.Group()
        self.bgsurfrect = pygame.Rect((0,0,0,0)) #needs to be initialized for now
        self.roomlinks = []
        self.doorlist = {}

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
        self.bgsurfrect.x += shift_x

#######################################
#                                     #
#        Actual Levels                #
#                                     #
#######################################
class Level01(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_limit_r = -1200
        self.level_limit_l = 1200
        self.bglist = []
        self.bgimglist = ['../images/lv1bg1sky.png', '../images/lv1bg2mntfar.png', '../images/lv1bg3mntmid.png', '../images/lv1bg4mntnear.png']

        ##########################
        #  background images     #
        ##########################
        self.bgsurf = pygame.Surface((4000, 600))
        self.bgimage = pygame.image.load('../images/level1bg.png')
        self.bgrect = self.bgimage.get_rect()
        self.bgsurf.blit(self.bgimage, self.bgrect)
        self.bgsurfrect = self.bgsurf.get_rect(x=-1200)

        # a list of platforms........
        #           width  X     Y  of top left
        platforms = [[210, 500, 500],
                [210, 200, 400],
                [210, 600, 300],
                [210, 100, 100],
                [420, 1000, SCREENH/2],
                [600,   0,  SCREENH-PLATFORMH]
                ]
        for platform in platforms:  #for each element of level, create a platform
            block = Platform((platform[0], PLATFORMH))
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            self.platform_list.add(block) #and add it to platform list

        #########################
        #  special blocks       #
        #########################
        gravityblock = GravityBlock()
        gravityblock.rect.x = 200
        gravityblock.rect.y = 336

        speedblock = SpeedBlock()
        speedblock.rect.x = 600
        speedblock.rect.y = 250
        self.special_blocks.add(gravityblock, speedblock)

        #########################
        #  event blocks         #
        #########################
        doorblock = DoorBlock("starting door", (200, SCREENH-160), "first room", "first door")
        self.special_blocks.add(doorblock)
        self.doorlist[doorblock.name] = doorblock

    def draw(self):
        SCREEN.fill(WHITE)
        SCREEN.blit(self.bgsurf, self.bgsurfrect)
        self.platform_list.draw(SCREEN)
        self.enemy_list.draw(SCREEN)
        self.special_blocks.draw(SCREEN)
        self.bullet_list.draw(SCREEN)

class Level02(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_limit_r = -1000
        self.level_limit_l = 1000

        platforms = [[110, 70, 520, 400],  #a list of platform rect-style  lists
                [110, 70, 200, 400],
                [110, 70, 600, 300],
                [110, 70, 100, 100],
                [120, 70, 1000, SCREENH/2],
                ]
        for platform in platforms:  #for each element of level, create a platform
            block = Platform((platform[0], platform[1]))
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block) #and add it to platform list

        #Create gravity block and add it to the special_blocks list
        gravityblock = GravityBlock()
        gravityblock.rect.x = 250
        gravityblock.rect.y = 336

        #creates a speed powerup block and adds it to the list
        speedblock = SpeedBlock()
        speedblock.rect.x = -100
        speedblock.rect.y = SCREENH - 77
        self.special_blocks.add(gravityblock, speedblock)

        ########################
        #   event blocks       #
        ########################
        self.doorblock = DoorBlock("first door", (300,SCREENH-128), "starting", "starting door")
        self.special_blocks.add(self.doorblock)
        self.doorlist[self.doorblock.name] = self.doorblock

    def draw(self):

        SCREEN.fill(GREEN)
        self.platform_list.draw(SCREEN)
        self.enemy_list.draw(SCREEN)
        self.special_blocks.draw(SCREEN)
        self.bullet_list.draw(SCREEN)
        #self.all_sprites_list.draw(SCREEN)


class Blank(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_limit_r = None
        self.level_limit_l = None

        ##########################
        # Background Handling    #
        ##########################
        self.background = None

        platforms = []

        for platform in platforms:
            pass

        def draw(self):
            pass

mainlist = { "starting" : Level01(),
             "first room" : Level02(),

             }
