import pygame
from eventmanager import PlayerMoveEvent, PlayerStopMovingEvent, TickEvent

class Trent(pygame.sprite.Sprite):

    def __init__(self, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.image = pygame.image.load('images/trent.png')
        self.image.convert_alpha()
        self.x = 100
        self.y = 256
        self.rect = self.image.get_rect(x=self.x, y=self.y)
        self.dx = 0

    def notify(self, event):
        if isinstance(event, TickEvent):
            self.rect.x += self.dx
        elif isinstance(event, PlayerMoveEvent):
            if event.direction == 'right':
                self.dx = 8
            elif event.direction == 'left':
                self.dx -= 8
        elif isinstance(event, PlayerStopMovingEvent):
            self.dx = 0

class Woman(pygame.sprite.Sprite):

    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load('images/woman.png')
        self.image.convert_alpha()
        self.x = 500
        self.y = 256
        self.rect = self.image.get_rect(x=self.x, y=self.y)

