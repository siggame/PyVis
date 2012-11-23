from pyglet import graphics
from pyglet import gl
from pyglet import clock
'''
'''
# Prohibit from renderer import *
__all__ = []


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

    def init_frame(self):
        self.frame = graphics.Batch()

    def draw_frame(self):
        self.frame.draw()
        self.fps_display.draw()

    def build_rect(self, x, y, width, height, group=None):
        '''
        '''

        data = [
            ('v2f',
                (x, y,
                 x + width, y,
                 x + width, y + height,
                 x, y + height)),
            ('c4f',
                (self.fg_color) * 4)]

        if self.texture:
            data += [
                ('t2f',
                    (0, 0,
                     1, 0,
                     1, 1,
                     0, 1))]
            group = graphics.TextureGroup(self.texture, parent=group)

        self.frame.add(4, gl.GL_QUADS, group, *data)
