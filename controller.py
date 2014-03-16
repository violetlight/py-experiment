import pygame
import model
from eventmanager import *

class Keyboard(object):
    def __init__(self, evManager, model):
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

    def notify(self, event):
        if isinstance(event, TickEvent):
            for event in pygame.event.get():
                #Quit
                if event.type == pygame.QUIT:
                    self.evManager.Post(QuitEvent())
                #Keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.evManager.Post(StateChangeEvent(None))
                    else:
                        currentstate = self.model.state.peek()
                        if currentstate == model.STATE_MENU:
                            self.keydownmenu(event)
                        if currentstate == model.STATE_PLAY:
                            self.keydownplay(event)
                        if currentstate == model.STATE_HELP:
                            self.keydownhelp(event)

    def keydownmenu(self, event):
        if event.key == pygame.K_ESCAPE:
            self.evManager.Post(StateChangeEvent(None))
        if event.key == pygame.K_SPACE:
            self.evManager.Post(StateChangeEvent(model.STATE_PLAY))

    def keydownhelp(self, event):
        if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
            self.evManager.Post(StateChangeEvent(None))

    def keydownplay(self, event):
        if event.key == pygame.K_ESCAPE:
            self.evManager.Post(StateChangeEvent(None))
        if event.key == pygame.K_F1:
            self.evManager.Post(StateChangeEvent(model.STATE_HELP))
        else:
            self.evManager.Post(InputEvent(event.unicode, None))
