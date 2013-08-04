#!/bin/env python
from __future__ import print_function
from pyz.application import Application
from pyz.renderer import Renderer
from argparse import ArgumentParser
import math

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
        self.p = 0

        self.e = 0
        self.s = 0

        from pyz import progress_bar

        self.pb = progress_bar.ProgressBar(renderer, 20, 120, 420, 5, 0.76)

        self.pie_1 = renderer.Arc(150, 230, 50, points=12, start=0, end=45, filled=True, loop=False, color=(1, 0, 0, 0))
        self.pie_2 = renderer.Arc(150, 230, 50, points=12, start=45, end=275, filled=True, loop=False, color=(0, 1, 0, 0))
        self.pie_2 = renderer.Arc(150, 230, 50, points=12, start=275, end=360, filled=True, loop=False, color=(0, 0, 1, 0))

        # for x in range(40):
        #     for y in range(30):
        #         y += 20
        #         if (x + y) % 3 == 0:
        #             self.renderer.fg_color = (1, 0, 0, 1)
        #         elif (x + y) % 3 == 1:
        #             self.renderer.fg_color = (0, 1, 0, 1)
        #         else:
        #             self.renderer.fg_color = (0, 0, 1, 1)
        #         self.batches += [renderer.Rectangle(x * 10, y * 10, 10, 10)]

    def update(self):

        self.pb.update_progress(self.p)

        self.p += 0.0001

        self.e += 0.03
        self.s += 0.02

        if self.e > 360:
            self.e = 0

        if self.s > 360:
            self.s = 0

        # self.arc.end = round(self.e)
        # self.arc.start = round(self.s)

        if self.p > 1:
            self.p = 0

        pass
        # for b in self.batches:
        #     b.x += 1
        #    b.draw()


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

    app.request_update_on_draw(Test(app.renderer).update)

    from pyz.gui import GUI

    gui = GUI(app)

    frame = gui.add_frame()
    button = gui.Button(app.renderer, gui, 100, 300, 100, 30, "Button",
        color=(0.0, 0.75, 0.2, 1.0))
    frame.add_child(button)


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
