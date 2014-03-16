import pygame
import model
from eventmanager import *

class GameScreen(object):
    def __init__(self, evManager, model):
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None

    def notify(self, event):
        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            self.renderall()
            self.clock.tick(30)

    def renderall(self):
        if not self.isinitialized:
            return
        self.screen.fill((0,0,0))
        test_text = self.smallfont.render(
                'importado y distribudo',
                True,
                (128, 255, 128))
        self.screen.blit(test_text, (0, 0))
        pygame.display.flip()

    def initialize(self):
        result = pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Sketchbook')
        self.screen = pygame.display.set_mode((600, 100))
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font(None, 40)
        self.isinitialized = True
