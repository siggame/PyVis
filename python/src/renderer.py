from pyglet.window import Window

# Prohibit from renderer import *
__all__ = []

class Renderer(object):
    def __init__(self, application):
        self.app = application
