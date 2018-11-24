import pyglet
from primitives import Rectangle, Line
from const import *
from enums import *



class Badge(object):
    HEIGHT = 20
    WIDTH_MARGIN = 16
    FONT_SIZE = 11


    def __init__(self, location, text, border, background):
        self.batch = pyglet.graphics.Batch()
        self.location = location
        self.state = ControlState.DEFAULT

        self.border_color = {
            ControlState.DEFAULT: border,
            ControlState.HOVER: (min(border[0] + 30, 255), min(border[1] + 30, 255), min(border[2] + 30, 255), 255)
        }

        self.background_color = {
            ControlState.DEFAULT: background,
            ControlState.HOVER: background
        }

        self.label = pyglet.text.Label(text, FONT, Badge.FONT_SIZE, color=CT_OFFWHITE,
                                       x=location[0] + Badge.WIDTH_MARGIN, y=location[1] - 1 - Badge.HEIGHT // 2,
                                       height=Badge.HEIGHT, anchor_y='center', bold=True,
                                       multiline=False, batch=self.batch)

        self.size = (Badge.WIDTH_MARGIN * 2 + self.label.content_width, Badge.HEIGHT)

        self.background = Rectangle(
            self.batch, None, self.location[0], self.location[1],
            self.location[0] + self.size[0], self.location[1] - self.size[1], self._get_background()
        )

        # Border is comprised of 4 line segments (left, top, right, bottom)
        self.border = [
            Line(self.batch, None, self.location, (self.location[0], self.location[1] - self.size[1]), 1,
                 self._get_border()),
            Line(self.batch, None, self.location, (self.location[0] + self.size[0], self.location[1]), 1,
                 self._get_border()),
            Line(self.batch, None, (self.location[0] + self.size[0], self.location[1]),
                 (self.location[0] + self.size[0],
                  self.location[1] - self.size[1]), 1, self._get_border()),
            Line(self.batch, None, (self.location[0], self.location[1] - self.size[1]),
                 (self.location[0] + self.size[0],
                  self.location[1] - self.size[1]), 1, self._get_border()),
        ]


    def _get_background(self):
        return self.background_color[self.state]

    def _get_border(self):
        return self.border_color[self.state]

    def draw(self):
        self.batch.draw()
