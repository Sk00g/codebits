import pyglet
from enums import *
from primitives import Rectangle, Line


class Button(object):
    def __init__(self, batch, icon, location, size, background, border_color, border_thickness=1):
        self.batch = batch
        self.location = location
        self.size = size
        self.icon = icon
        self.default_border = border_color
        self.hover_border = border_color
        self.pressed_border = border_color
        self.default_bkgr = background
        self.hover_bkgr = background
        self.pressed_bkgr = background
        self.state = ButtonState.DEFAULT

        self.bkgr_rect = Rectangle(
            batch, location[0], location[1],
            location[0] + size[0], location[1] + size[1], background
        )

        # Border is comprised of 4 line segments (left, top, right, bottom)
        self.border = [
            Line(batch, location, (location[0], location[1] + size[1]), border_thickness, border_color),
            Line(batch, location, (location[0] + size[0], location[1]), border_thickness, border_color),
            Line(batch, (location[0] + size[0], location[1]), (location[0] + size[0], location[1] + size[1]),
                 border_thickness, border_color),
            Line(batch, (location[0], location[1] + size[1]), (location[0] + size[0], location[1] + size[1]),
                 border_thickness, border_color),
        ]

        self.sprite = pyglet.sprite.Sprite(icon, location[0] + 8, location[1] + 8, batch=self.batch)
        self.sprite.scale = 0.4

    def _change_state(self, new_state):
        if self.state == new_state:
            return

        self.state = new_state
        if new_state == ButtonState.HOVER:
            self.bkgr_rect.set_color(self.hover_bkgr)
            for line in self.border:
                line.set_color(self.hover_border)
        elif new_state == ButtonState.DEFAULT:
            self.bkgr_rect.set_color(self.default_bkgr)
            for line in self.border:
                line.set_color(self.default_border)
        elif new_state == ButtonState.PRESSED:
            self.bkgr_rect.set_color(self.pressed_bkgr)
            for line in self.border:
                line.set_color(self.pressed_border)

    def handle_mouse(self, x, y):
        if (0 < x - self.location[0] < self.size[0] and
                0 < y - self.location[1] < self.size[1]):
            self._change_state(ControlState.HOVER)
        else:
            self._change_state(ControlState.DEFAULT)

    def handle_mouse_press(self, x, y):
        if (0 < x - self.location[0] < self.size[0] and
                0 < y - self.location[1] < self.size[1]):
            self._change_state(ButtonState.PRESSED)