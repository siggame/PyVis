from application import Application
from renderer import Renderer

# Prohibit from main import *
__all__ = []

def main():

    app = Application()
    renderer = Renderer(app)

    app.run()

if __name__ == '__main__':
    main()
