import pygame

class Decor(pygame.sprite.Sprite):

    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load('images/tree.png')
        self.image.convert_alpha()
        self.x = 200
        self.y = -48
        self.rect = self.image.get_rect(x=self.x, y=self.y)

