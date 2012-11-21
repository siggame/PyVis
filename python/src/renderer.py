from pyglet.window import Window

# Prohibit from renderer import *
__all__ = []

class Renderer(object):
    def __init__(self, application):
        self.app = application

    '''
        @application.window.event
        def on_draw():
            self.on_draw()

    def on_draw(self):
        self.app.window.clear() 
        print('Renderering')
    '''
