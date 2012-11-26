from application import Application
from renderer import Renderer, Rectangle

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
                self.batches += [Rectangle(self.renderer, x * 10, y * 10, 10, 10)]

    def update(self):
        '''
        for b in self.batches:
            b.draw()
        '''


def main():
    app = Application()
    renderer = Renderer(app)
    app.request_update_on_draw(renderer.draw_frame, 100)
    app.request_update_on_draw(renderer.init_frame, 0)
    app.request_update_on_draw(Test(renderer).update)

    r = Rectangle(renderer, 1, 2, 20, 30)
    r = Rectangle(renderer, 40, 40, 20, 30)

    app.run()

if __name__ == '__main__':
    main()
