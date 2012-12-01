
class TrackObject(object):
    def __init__(self):
        pass

class Track(object):
    '''
    Track is a container object 
    '''
    life = 0
    death = float('Inf')

    def __init__(self):
        pass


class Timeline(object):
    tracks = []
    def __init__(self):
        pass

    def add(self, obj):
        t = Track(obj)
        obj.track = t
        tracks += [t]


timeline.add(self, Ship(states))

timeline = Timeline()

ship = t.add(Ship)

ship.move()


