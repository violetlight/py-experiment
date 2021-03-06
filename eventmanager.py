class Event(object):
    def __init__(self):
        self.name = "Generic event"
    def __str__(self):
        return self.name

class QuitEvent(Event):
    def __init__(self):
        self.name = "Quit event"

class TickEvent(Event):
    def __init__(self):
        self.name = "Tick event"

class InputEvent(Event):
    def __init__(self, unicodechar, clickpos):
        self.name = "Input event"
        self.char = unicodechar
        self.clickpos = clickpos
    def __str__(self):
        return '%s, char=%s, clickpos=%s' % (self.name, self.char, self.clickpos)

class InitializeEvent(Event):
    def __init__(self):
        self.name = "Initialize event"

class StateChangeEvent(Event):
    def __init__(self, state):
        self.name = "State Change event"
        self.state = state

    def __str__(self):
        if self.state:
            return '%s pushed %s' % (self.name, self.state)
        else:
            return '%s popped' % self.name

#######################################
#
#   Player motion
#
#######################################
class PlayerMoveEvent(Event):
    def __init__(self, direction):
        self.name = "Player Move Event"
        self.direction = direction

class PlayerStopMovingEvent(Event):
    def __init__(self):
        self.name = "Player Stop Moving Event"

#######################################
#
#    Event Manager
#
#######################################
class EventManager(object):
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def RegisterListener(self, listener):
        self.listeners[listener] = 1

    def UnregisterListener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[listener]

    def Post(self, event):
        if not isinstance(event, TickEvent):
            print(str(event))
        for listener in self.listeners.keys():
            listener.notify(event)
