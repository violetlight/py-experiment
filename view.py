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
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == model.STATE_MENU:
                self.rendermenu()
            if currentstate == model.STATE_PLAY:
                self.renderplay()
            if currentstate == model.STATE_HELP:
                self.renderhelp()
            self.clock.tick(30)

    def rendermenu(self):
        self.screen.fill((0,0,0))
        words = self.smallfont.render(
                "You are in the Menu. Space to play. Esc exits.",
                True,
                (64,64,128))
        self.screen.blit(words, (0,0))
        pygame.display.flip()

    def renderplay(self):
        self.screen.fill((30,30,30))
        #here
        from maps import MAP, TILESET
        self.background = pygame.Surface(self.screen.get_size())
        for row in range(len(MAP)):
            for col in range(len(MAP[row])):
                location = (col*32, row*32)
                self.background.blit(TILESET, location, MAP[row][col])
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

    def renderhelp(self):
        self.screen.fill((0,0,0))
        words = self.smallfont.render(
                "This is help. Space, Esc, or Enter",
                True,
                (128, 64, 64))
        self.screen.blit(words, (0,0))
        pygame.display.flip()

    def initialize(self):
        result = pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Sketchbook')
        #Screen creation
        self.screen = pygame.display.set_mode((640,480))
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font(None, 40)
        self.isinitialized = True
