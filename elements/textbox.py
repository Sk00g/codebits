import pyglet
from pyglet.window import key, mouse
from const import *
from enums import *
from primitives import Rectangle, Line


class TextBox(object):
    def __init__(self, window, batch, location, size, border_color, border_thickness=1, background=(0, 0, 0, 0)):
        self.host_window = window
        self.batch = batch
        self.location = location
        self.size = size
        self.state = ControlState.DEFAULT

        # Set values based on state
        self.border_color = {
            ControlState.DEFAULT: border_color,
            ControlState.DISABLED: CT_WHITE2,
            ControlState.FOCUS: CT_NEARWHITE,
            ControlState.HOVER: CT_NEARWHITE
        }
        self.background_color = {
            ControlState.DEFAULT: background,
            ControlState.DISABLED: background,
            ControlState.FOCUS: background,
            ControlState.HOVER: background
        }

        self.background = Rectangle(
            batch, location[0], location[1],
            location[0] + size[0], location[1] + size[1], self._get_background()
        )

        # Border is comprised of 4 line segments (left, top, right, bottom)
        self.border = [
            Line(batch, location, (location[0], location[1] + size[1]), border_thickness, self._get_border()),
            Line(batch, location, (location[0] + size[0], location[1]), border_thickness, self._get_border()),
            Line(batch, (location[0] + size[0], location[1]), (location[0] + size[0], location[1] + size[1]), border_thickness, self._get_border()),
            Line(batch, (location[0], location[1] + size[1]), (location[0] + size[0], location[1] + size[1]), border_thickness, self._get_border()),
        ]

        # Formatted document stores the formatting and text
        self.document = pyglet.text.document.FormattedDocument(' ')
        self.document.set_style(0, 1, dict(color=BOX_TEXT_COLOR, font_name=FONT, font_size=BOX_FONT_SIZE))
        self.document.text = ''

        # IncrementalLayout handles displaying the document
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                                               size[0], size[1],
                                                               multiline=True, batch=self.batch)
        self.layout.x = location[0] + 10
        self.layout.y = location[1] - 8
        self.layout.selection_color = CT_NEARWHITE
        self.layout.selection_background_color = CT_PRIMARY['search']

        # Caret provides basic text entry functionality
        self.caret = pyglet.text.caret.Caret(self.layout, color=BOX_CARET_COLOR)
        self.caret.position = 0
        self.caret.mark = None
        self.caret.visible = False


    def _get_background(self):
        return self.background_color[self.state]

    def _get_border(self):
        return self.border_color[self.state]

    # Updates colors and other styles based on current state
    def _update_style(self):
        for line in self.border:
            line.set_color(self._get_border())

        self.background.set_color(self._get_background())

        self.caret.visible = True if self.state == ControlState.FOCUS else False

    def _change_state(self, new_state):
        if self.state == new_state:
            return

        self.state = new_state
        self._update_style()

        # Special text-caret functionality
        # self.caret.on_mouse_press(self.location[0], self.location[1], mouse.LEFT, 0)

    def handle_mouse_motion(self, x, y):
        if (0 < x - self.location[0] < self.size[0] and
            0 < y - self.location[1] < self.size[1]):
            # Only change to hover state if we are in DEFAULT
            if self.state == ControlState.DEFAULT:
                self._change_state(ControlState.HOVER)
                self.host_window.set_mouse_cursor(self.host_window.get_system_mouse_cursor('text'))
        else:
            # Only change back from hover state if mouse leaves
            if self.state == ControlState.HOVER:
                self._change_state(ControlState.DEFAULT)
                self.host_window.set_mouse_cursor(self.host_window.get_system_mouse_cursor(pyglet.window.Window.CURSOR_DEFAULT))

    def alter_focus(self, flag):
        # Cannot focus disabled controls
        if self.state == ControlState.DISABLED:
            return

        if flag:
            if self.state != ControlState.FOCUS:
                self._change_state(ControlState.FOCUS)
        else:
            if self.state == ControlState.FOCUS:
                self._change_state(ControlState.DEFAULT)

    def handle_mouse_press(self, x, y, button, modifiers):
        if (0 < x - self.location[0] < self.size[0] and
            0 < y - self.location[1] < self.size[1]):
            if self.state != ControlState.FOCUS:
                self.caret.position = len(self.document.text)
                self._change_state(ControlState.FOCUS)
            else:
                self.caret.on_mouse_press(x, y, button, modifiers)

            return True


    def handle_mouse_release(self, x, y, button, modifiers):
        pass

    def handle_key_press(self, symbol, modifiers):
        if self.state == ControlState.FOCUS:
            if symbol == key.A and modifiers & key.MOD_CTRL:
                self.caret.position = 0
                self.caret.mark = len(self.document.text)

    def handle_key_release(self, symbol, modifiers):
        pass

    # Format visual style and run suggestion / template language algorithms on each change
    def update_entry(self):
        # print('position: %d || mark: %s || text: %s' % (self.caret.position, self.caret.mark, self.document.text))
        text = self.document.text
        words = text.split(' ')
        for id in range(0, len(text) - 1):
            if text[id].isupper() and id in [text.find(word) for word in words if len(word) > 1]:
                print('adding purple')
                self.document.set_style(id, id + 1, dict(color=CT_PRIMARY['search']))
            else:
                self.document.set_style(id, id + 1, dict(color=CT_OFFWHITE))


    # Text entry mouse and keyboard events
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.state == ControlState.FOCUS:
            self.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
            self.update_entry()

    def on_text(self, text):
        if self.state == ControlState.FOCUS:
            self.caret.on_text(text)
            self.update_entry()

    def on_text_motion(self, motion):
        if self.state == ControlState.FOCUS:
            self.caret.on_text_motion(motion)
            self.update_entry()

    def on_text_motion_select(self, motion):
        if self.state == ControlState.FOCUS:
            self.caret.on_text_motion_select(motion)
            self.update_entry()

