import pygame
from eventmanager import *

class Engine(object):

    def __init__(self, evManager):
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.running = False

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.running = False

    def run(self):
        self.running = True
        self.evManager.Post(InitializeEvent())
        while self.running:
            next_tick = TickEvent()
            self.evManager.Post(next_tick)
