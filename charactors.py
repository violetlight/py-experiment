import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load('images/charactorsprite.png')
        self.image.convert_alpha()
        self.x = 100
        self.y = 256
        self.rect = self.image.get_rect(x=self.x, y=self.y)

