#!/bin/env python
from __future__ import print_function
from application import Application
from renderer import Renderer
from argparse import ArgumentParser

# Prohibit from main import *
__all__ = []


class GameObject(object):
    pass


class TimelineObject(object):
    pass


class Ship(GameObject, TimelineObject):
    pass


class Test:
    def __init__(self, renderer):
        self.renderer = renderer
        self.batches = []
        for x in range(40):
            for y in range(30):
                y += 20
                if (x + y) % 3 == 0:
                    self.renderer.fg_color = (1, 0, 0, 1)
                elif (x + y) % 3 == 1:
                    self.renderer.fg_color = (0, 1, 0, 1)
                else:
                    self.renderer.fg_color = (0, 0, 1, 1)
                self.batches += [renderer.Rectangle(x * 10, y * 10, 10, 10)]

    def update(self):
        '''
        for b in self.batches:
            b.draw()
        '''


def main():

    parser = ArgumentParser(description=
        'MegaMinerAI PyVis - Python Implementation of the Visualizer')
    parser.add_argument('glog', type=str, nargs='*', 
            help='Optional glogs to open in the visualizer.')
    parser.add_argument('-f', dest='fullscreen', action='store_true', 
            help='Start in fullscreen mode')
    parser.add_argument('-a', dest='arena', metavar='server', type=str, nargs=1, 
            help='Enables arena mode querying from the given url')
    parser.add_argument('-s', dest='spectate', 
            metavar=('server', 'gamenumber'), nargs=2, type=str, 
            help='Spectates on gamenumber at server.')

    args = parser.parse_args()

    app = Application(fullscreen=args.fullscreen)
    '''
    renderer = Renderer()
    renderer.register_with_app(app)
    app.request_update_on_draw(Test(renderer).update)

    r = Renderer.Rectangle(1, 2, 20, 30, renderer=renderer)
    try:
        r = Renderer.Rectangle(40, 40, 20, 30)
    except:
        pass
    '''

    app.run(args.glog)

if __name__ == '__main__':
    main()
