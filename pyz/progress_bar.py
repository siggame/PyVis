import renderer

class ProgressBar(renderer.Composite):
    def __init__(self, renderer, x, y, width, height, progress, horizontal=True):
        super(ProgressBar, self).__init__(renderer)

        self._width = width
        self._height = height
        self._progress = progress
        self.horizontal = horizontal

        self.outline = renderer.Rectangle(0, 0, width, height, filled=False,
            color=renderer.bg_color, offset=(x, y))
        self.bar = renderer.Rectangle(0, 0, width, height,
            color=renderer.fg_color, offset=(x, y))

        self.update_progress(progress)

    def update_progress(self, progress):
        if self.horizontal:
            width = (self.width) * progress
            height = (self.height)
        else:
            width = (self.width)
            height = (self.height) * progress

        self.bar.transform(scale=(width, height))

    progress = property(
        lambda self: self._progress,
        lambda self, progress: self.update_progress(progress)
        )
