from application import Application
from renderer import Renderer

# Prohibit from main import *
__all__ = []


class Test:
    def __init__(self, renderer):
        self.renderer = renderer

    def update(self):
        for x in range(40):
            for y in range(30):
                if (x + y) % 3 == 0:
                    self.renderer.fg_color = (1, 0, 0, 1)
                elif (x + y) % 3 == 1:
                    self.renderer.fg_color = (0, 1, 0, 1)
                else:
                    self.renderer.fg_color = (0, 0, 1, 1)
                self.renderer.drawRect(x * 10, y * 10, 10, 10)


def main():
    app = Application()
    renderer = Renderer(app)
    app.request_update_on_draw(renderer.init_frame)
    app.request_update_on_draw(Test(renderer).update)
    app.request_update_on_draw(renderer.draw_frame)

    app.run()

if __name__ == '__main__':
    main()
