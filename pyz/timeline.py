'''
oifjak faslkjas iofjas osjfoasifja sfjasdlk
'''

class TrackObject(object):
    '''
    This is the base class
    '''
    life = 0
    death = float('Inf')

    def __init__(self, timeline):
        self.timeline = timeline

    def move():
        pass

class Timeline(object):
    '''
    Timeline
    '''
    tracks = []
    def __init__(self):
        pass

    def add(self, obj):
        assert issubclass(obj.__class__, TrackObject)
        t = Track(obj)
        obj.track = t
        tracks += [t]

'''
ship = Ship(timeline, 
ship = timeline.add(Ship(states))


timeline = Timeline()

ship = t.add(Ship)

ship.move()


'''
