import pyglet
from const import *
from enums import *
from primitives import Rectangle, Line


class TextBox(object):
    def __init__(self, batch, location, size, border_color, border_thickness=1, background=(0, 0, 0, 0)):
        self.batch = batch
        self.location = location
        self.size = size
        self.state = ControlState.DEFAULT
        self.default_border_color = border_color
        self.hover_border_color = None
        self.hover_bkgr = None

        self.default_bckg_rect = Rectangle(
            batch, location[0], location[1],
            location[0] + size[0], location[1] + size[1], background
        )

        # Border is comprised of 4 line segments (left, top, right, bottom)
        self.border = [
            Line(batch, location, (location[0], location[1] + size[1]), border_thickness, border_color),
            Line(batch, location, (location[0] + size[0], location[1]), border_thickness, border_color),
            Line(batch, (location[0] + size[0], location[1]), (location[0] + size[0], location[1] + size[1]), border_thickness, border_color),
            Line(batch, (location[0], location[1] + size[1]), (location[0] + size[0], location[1] + size[1]), border_thickness, border_color),
        ]

        # Formatted document stores the formatting and text
        self.document = pyglet.text.document.FormattedDocument(' ')
        self.document.set_style(0, 0, dict(color=BOX_TEXT_COLOR, font_name=FONT, font_size=BOX_FONT_SIZE))

        # IncrementalLayout handles displaying the document
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                                               size[0], size[1],
                                                               multiline=True, batch=self.batch)

        # Caret provides basic text entry functionality
        self.caret = pyglet.text.caret.Caret(self.layout, color=BOX_CARET_COLOR)
        self.caret.position = 0
        self.caret.mark = 0
        self.caret.visible = True

        self.layout.x = location[0]
        self.layout.y = location[1]

    def _change_state(self, new_state):
        if self.state == new_state:
            return

        self.state = new_state
        if new_state == ControlState.HOVER:
            for line in self.border:
                line.set_color(self.hover_border_color)
        elif new_state == ControlState.DEFAULT:
            for line in self.border:
                line.set_color(self.default_border_color)

    def handle_mouse(self, x, y):
        if (0 < x - self.location[0] < self.size[0] and
            0 < y - self.location[1] < self.size[1]):
            self._change_state(ControlState.HOVER)
            return True
        else:
            self._change_state(ControlState.DEFAULT)
            return False

    def handle_mouse_press(self, x, y, button, modifiers):
        if (0 < x - self.location[0] < self.size[0] and
            0 < y - self.location[1] < self.size[1]):
            self.caret.on_mouse_press(x, y, button, modifiers)