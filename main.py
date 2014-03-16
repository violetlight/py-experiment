#!/usr/bin/env python2

import eventmanager, model, view, controller
#import model
#import view
#import controller


def run():
    evManager = eventmanager.EventManager()
    gamemodel = model.Engine(evManager)
    keyboard = controller.Keyboard(evManager, gamemodel)
    graphics = view.GameScreen(evManager, gamemodel)
    gamemodel.run()

if __name__ == '__main__':
    run()
