from pyglet.window import Window
import pyglet

# Prohibit from application import *
__all__ = []

DEFAULT_WIDTH = 640 
DEFAULT_HEIGHT = 480

class Application(object):
    def __init__(self, size=(DEFAULT_WIDTH, DEFAULT_HEIGHT), 
            title='MegaMinerAI Bland Title Text', fullscreen=False):
        self.window = Window(width=size[0], height=size[1], caption=title,
                visible=True, fullscreen=fullscreen, resizable=True,
                style=Window.WINDOW_STYLE_DEFAULT, vsync=True, display=None,
                context=None, config=None)

    def update(self, dt):
        # Forces a redraw
        # Trigger everything 

        self.window.clear()

        pass

    def run(self):
        pyglet.clock.schedule(self.update)
        pyglet.app.run()
