from pyglet import graphics
from pyglet import gl
from pyglet import clock
'''
'''
# Prohibit from renderer import *
__all__ = []


class Primitive(object):
    def draw(self):
        for i, j in zip(self.vertex_lists, self.modes):
            pass
            # self.renderer.frame.add(4, j, None, *i)


class Rectangle(Primitive):
    def __init__(self, renderer, x, y, width, height, group):
        self.renderer = renderer
        data = [('v2f', (x, y, x + width, y,
                 x + width, y + height,
                 x, y + height)),
            ('c4f',
                (renderer.fg_color) * 4)]

        if renderer.texture:
            data += [
                ('t2f',
                    (0, 0,
                     1, 0,
                     1, 1,
                     0, 1))]
            group = graphics.TextureGroup(renderer.texture, parent=group)

        self.vertex_lists = [data]

        self.modes = [gl.GL_QUADS]


class Renderer(object):
    '''
    '''

    fg_color = (1, 0, 0, 1)
    bg_color = (0, 0, 1, 1)
    texture = None

    def __init__(self, application):
        '''
        '''
        self.app = application
        self.fps_display = clock.ClockDisplay()
        self.init_frame()

    def init_frame(self):
        self.frame = graphics.Batch()

    def draw_frame(self):
        self.frame.draw()
        self.fps_display.draw()

    def build_rect(self, x, y, width, height, group=None):
        '''
        '''

        return Rectangle(self, x, y, width, height, group)

