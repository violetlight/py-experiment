from __future__ import print_function
import pygame
from eventmanager import *

class Engine(object):

    def __init__(self, evManager):
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.running = False
        self.state = StateMachine()

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.running = False
        if isinstance(event, StateChangeEvent):
            if not event.state:
                if not self.state.pop():
                    self.evManager.Post(QuitEvent())
            else:
                self.state.push(event.state)

    def run(self):
        self.running = True
        self.evManager.Post(InitializeEvent())
        self.state.push(STATE_MENU)
        while self.running:
            next_tick = TickEvent()
            self.evManager.Post(next_tick)

#State machine constants
STATE_INTRO = 1
STATE_MENU  = 2
STATE_HELP  = 3
STATE_ABOUT = 4
STATE_PLAY  = 5

class StateMachine(object):
    def __init__(self):
        self.statestack = []

    def peek(self):
        try:
            return self.statestack[-1]
        except IndexError:
            return None

    def pop(self):
        try:
            self.statestack.pop()
            return len(self.statestack) > 0
        except IndexError:
            return None

    def push(self, state):
        self.statestack.append(state)
        return state
