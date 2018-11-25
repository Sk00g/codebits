import pyglet
from swidget import UIElement, ControlElement, Rectangle, Line, Label, ControlState
from swidget.theme import Basic


class Badge(ControlElement, pyglet.event.EventDispatcher):
    PADDING_WIDTH = 14
    PADDING_HEIGHT = 2

    def __init__(self, batch, text="badge", click_event=None, position=(0, 0), group=None, visible=True):
        default_style = {
            ControlState.DEFAULT: {
                "border_thickness": 1,
                "border_color": Basic.PRIMARY,
                "font_color": Basic.OFFWHITE,
                "background_color": Basic.WHITE_TINGE1,
            },
            ControlState.HOVER: {
                "font_color": Basic.NEARWHITE,
                "background_color": Basic.PRIMARY_BRIGHT_TINGE
            },
            ControlState.DISABLED: {},
            ControlState.FOCUS: {},
            ControlState.PRESSED: {}
        }

        if click_event:
            self.push_handlers(on_click=click_event)

        self._group_back = pyglet.graphics.OrderedGroup(0, group)
        self._group_front = pyglet.graphics.OrderedGroup(1, group)

        self.label = Label(batch, text=text, group=self._group_front, font_color=Basic.OFFWHITE, font_size=10)
        size = self.label.get_size()[0] + Badge.PADDING_WIDTH, self.label.get_size()[1] + Badge.PADDING_HEIGHT
        self.background = Rectangle(batch, position, size, group=self._group_back)
        self.border = [
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front)
        ]

        ControlElement.__init__(self, batch, default_style, group, position, size, visible, False)

        self._render()

    def handle_mouse_press(self, x, y, button, modifiers):
        if self.is_point_within((x, y)):
            self.dispatch_event('on_click')

    def delete(self):
        self.background.delete()
        self.label.delete()
        for line in self.border:
            line.delete()

    def _render(self):
        self.background.set_size(self._size)
        self.background.set_position(self._position)

        pos = self._position
        size = self._size
        self.border[0].set_points(pos, (pos[0] + size[0], pos[1]))
        self.border[1].set_points((pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] + size[1]))
        self.border[2].set_points((pos[0] + size[0], pos[1]), (pos[0] + size[0], pos[1] + size[1]))
        self.border[3].set_points((pos[0], pos[1] + size[1]), (pos[0] + size[0], pos[1] + size[1]))

        self.label.center(pos[0] + size[0] // 2, pos[1] + size[1] // 2)

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

        # Label
        if "font_color" in style[state]:
            self.label.set_style(0, len(self.label.get_text()), dict(color=self.get_style(state, "font_color")))


Badge.register_event_type('on_click')



