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
                        self.evManager.Post(QuitEvent())
                    else:
                        self.evManager.Post(InputEvent(event.unicode, None))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.evManager.Post(InputEvent("Left click", None))
                    if event.button == 2:
                        self.evManager.Post(InputEvent("Mouse Wheel click", None))
                    if event.button == 3:
                        self.evManager.Post(InputEvent("Right click", None))

