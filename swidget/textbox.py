import pyglet
from swidget import ControlElement, Rectangle, Line, ControlState


class Textbox(ControlElement):
    def __init__(self, batch, position=(0, 0), size=(100, 20), font_size=12, group=None, visible=True):
        default_style = {
            ControlState.DEFAULT: {
                "border_thickness": 1,
                "border_color": (0xAA, 0xAA, 0xAA, 0xFF),
                "background_color": (255, 255, 255, 10)
            },
            ControlState.FOCUS: {
                "border_color": (0x00, 0x00, 0xEE, 0xFF),
            },
            ControlState.HOVER: {
                "border_color": (0xEE, 0xEE, 0xEE, 0xFF),
            },
            ControlState.DISABLED: {},
            ControlState.PRESSED: {}    # Unused in textbox
        }

        self._group_back = pyglet.graphics.OrderedGroup(0, group)
        self._group_front = pyglet.graphics.OrderedGroup(1, group)

        self.background = Rectangle(batch, position, size, group=self._group_back)
        self.border = [
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front)
        ]

        # Base class establishes style
        ControlElement.__init__(self, batch, default_style, group, position, size, visible)

    def delete(self):
        self.background.delete()

    def _render(self):
        self.background.set_size(self._size)
        self.background.set_position(self._position)

        pos = self._position
        size = self._size
        self.border[0].set_points(pos, (pos[0] + size[0], pos[1]))
        self.border[1].set_points((pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] + size[1]))
        self.border[2].set_points((pos[0] + size[0], pos[1]), (pos[0] + size[0], pos[1] + size[1]))
        self.border[3].set_points((pos[0], pos[1] + size[1]), (pos[0] + size[0], pos[1] + size[1]))

    def _apply_style(self):
        style = self._style
        state = self._state

        # Background
        if "background_color" in style[state]:
            self.background.set_color(self.get_style(state, "background_color"))

        # Border
        for line in self.border:
            if "border_thickness" in style[state]:
                line.set_thickness(self.get_style(state, "border_thickness"))
            if "border_color" in style[state]:
                line.set_color(self.get_style(state, "border_color"))

        # Font

        # Cursor

        # font size
        # cursor color
        pass
