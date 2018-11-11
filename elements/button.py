import pyglet
from pyglet.window import key
from const import *
from enums import *
from primitives import Rectangle, Line


class Button(object):
    def __init__(self, batch, icon, location, size, background, border_color, border_thickness=1):
        self.batch = batch
        self.location = location
        self.size = size
        self.icon = icon
        self.state = ButtonState.DEFAULT
        self.has_focus = False
        self.click_actions = []

        # Set values based on state
        self.border_color = {
            ButtonState.DEFAULT: border_color,
            ButtonState.DISABLED: CT_WHITE2,
            ButtonState.FOCUS: CT_NEARWHITE,
            ButtonState.HOVER: CT_NEARWHITE,
            ButtonState.PRESSED: CT_NEARWHITE
        }
        self.background_color = {
            ButtonState.DEFAULT: background,
            ButtonState.DISABLED: background,
            ButtonState.FOCUS: background,
            ButtonState.HOVER: CT_WHITE_TINGE2,
            ButtonState.PRESSED: CT_WHITE_TINGE3
        }

        self.background = Rectangle(
            batch, location[0], location[1],
            location[0] + size[0], location[1] + size[1], self._get_background()
        )

        # Border is comprised of 4 line segments (left, top, right, bottom)
        self.border = [
            Line(batch, location, (location[0], location[1] + size[1]), border_thickness, self._get_border()),
            Line(batch, location, (location[0] + size[0], location[1]), border_thickness, self._get_border()),
            Line(batch, (location[0] + size[0], location[1]), (location[0] + size[0], location[1] + size[1]),
                 border_thickness, self._get_border()),
            Line(batch, (location[0], location[1] + size[1]), (location[0] + size[0], location[1] + size[1]),
                 border_thickness, self._get_border()),
        ]

        self.sprite = pyglet.sprite.Sprite(icon, location[0] + 5, location[1] + 5, batch=self.batch)
        self.sprite.scale = 0.4

    def _get_background(self):
        return self.background_color[self.state]

    def _get_border(self):
        return self.border_color[self.state]

    # Updates colors and other styles based on current state
    def _update_style(self):
        for line in self.border:
            line.set_color(self._get_border())

        self.background.set_color(self._get_background())

    def _change_state(self, new_state):
        if self.state == new_state:
            return

        self.state = new_state
        self._update_style()

    def alter_focus(self, flag):
        # Cannot focus disabled or pressed controls
        if self.state == ButtonState.DISABLED or self.state == ButtonState.PRESSED:
            return

        if flag:
            if self.state != ButtonState.FOCUS:
                self._change_state(ButtonState.FOCUS)
            self.has_focus = True
        else:
            if self.state == ButtonState.FOCUS:
                self._change_state(ButtonState.DEFAULT)
            self.has_focus = False

    def handle_mouse_motion(self, x, y):
        if (0 < x - self.location[0] < self.size[0] and
                0 < y - self.location[1] < self.size[1]):
            # Only change to hover state if we are in DEFAULT
            if self.state == ButtonState.DEFAULT or self.state == ButtonState.FOCUS:
                self._change_state(ButtonState.HOVER)
        else:
            # Only change back from hover state if mouse leaves
            if self.state == ButtonState.HOVER:
                self._change_state(ButtonState.FOCUS if self.has_focus else ButtonState.DEFAULT)

    def handle_mouse_press(self, x, y, button, modifiers):
        if (0 < x - self.location[0] < self.size[0] and
                0 < y - self.location[1] < self.size[1]):
            self._change_state(ButtonState.PRESSED)
            return True

    def handle_mouse_release(self, x, y, button, modifiers):
        if (0 < x - self.location[0] < self.size[0] and
                0 < y - self.location[1] < self.size[1]):
            if self.state == ButtonState.PRESSED:
                self._change_state(ButtonState.HOVER)
                if self.click_actions:
                    for func in self.click_actions:
                        func()


    def handle_key_press(self, symbol, modifiers):
        if symbol == key.ENTER and self.state == ButtonState.FOCUS:
            self._change_state(ButtonState.PRESSED)

    def handle_key_release(self, symbol, modifiers):
        if symbol == key.ENTER and self.state == ButtonState.PRESSED:
            self._change_state(ButtonState.FOCUS if self.has_focus else ButtonState.DEFAULT)
            if self.click_actions:
                for func in self.click_actions:
                    func()