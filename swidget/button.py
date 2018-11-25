import pyglet
from pyglet.window import key
from swidget import UIElement, ControlElement, ControlState, Rectangle, Line, Image
from swidget.theme import Basic


class Button(ControlElement, pyglet.event.EventDispatcher):
    def __init__(self, batch, image_path, position=(0, 0), size=(20, 20), click_event=None, group=None, visible=True):
        default_style = {
            ControlState.DEFAULT: {
                "border_thickness": 1,
                "border_color": Basic.WHITE1,
                "background_color": Basic.WHITE_TINGE1,
            },
            ControlState.FOCUS: {
                "border_color": Basic.NEARWHITE,
                "background_color": Basic.WHITE_TINGE1
            },
            ControlState.HOVER: {
                "border_color": Basic.NEARWHITE,
                "background_color": Basic.WHITE_TINGE2
            },
            ControlState.DISABLED: {},
            ControlState.PRESSED: {
                "background_color": Basic.WHITE_TINGE3
            }
        }

        if click_event:
            self.push_handlers(on_click=click_event)

        self._group_back = pyglet.graphics.OrderedGroup(0, group)
        self._group_front = pyglet.graphics.OrderedGroup(1, group)

        self.background = Rectangle(batch, position, size, group=self._group_back)
        self.border = [
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front)
        ]

        self._image_path = image_path
        self.icon = Image(batch, image_path, position, size, self._group_front, visible)

        # Base class establishes style
        ControlElement.__init__(self, batch, default_style, group, position, size, visible)

        self._render()

    def delete(self):
        self.background.delete()
        for line in self.border:
            line.delete()
        self.icon.delete()

    def handle_mouse_press(self, x, y, button, modifiers):
        if self.is_point_within((x, y)):
            self._update_state(ControlState.PRESSED)

    def handle_mouse_release(self, x, y, button, modifiers):
        if self._state == ControlState.PRESSED:
            if self.is_point_within((x, y)):
                self._update_state(ControlState.HOVER)
            else:
                self._update_state(ControlState.FOCUS if self._has_focus else ControlState.DEFAULT)

            self.dispatch_event('on_click')


    def alter_focus(self, flag):
        # Cannot focus disabled or pressed controls
        if self._state == ControlState.DISABLED or self._state == ControlState.PRESSED:
            return

        if flag:
            if self._state != ControlState.FOCUS:
                self._update_state(ControlState.FOCUS)
            self._has_focus = True
        else:
            if self._state == ControlState.FOCUS:
                self._update_state(ControlState.DEFAULT)
            self._has_focus = False

    def get_image_path(self):
        return self._image_path

    def set_image_path(self, path):
        self._image_path = path
        self.icon.delete()
        self.icon = Image(self.batch, path, self._position, self._size, self._group_front, self._visible)

    def _render(self):
        self.background.set_size(self._size)
        self.background.set_position(self._position)

        pos = self._position
        size = self._size
        self.border[0].set_points(pos, (pos[0] + size[0], pos[1]))
        self.border[1].set_points((pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] + size[1]))
        self.border[2].set_points((pos[0] + size[0], pos[1]), (pos[0] + size[0], pos[1] + size[1]))
        self.border[3].set_points((pos[0], pos[1] + size[1]), (pos[0] + size[0], pos[1] + size[1]))

        self.icon.set_position(self._position)
        self.icon.set_size(self._size)

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

Button.register_event_type('on_click')