import pyglet
from pyglet.window import key
from swidget import UIElement, ControlElement, Rectangle, Line, ControlState
from swidget.theme import Basic


class Textbox(ControlElement, pyglet.event.EventDispatcher):
    BOX_LINE_HEIGHT = 19

    def __init__(self, batch, position=(0, 0), size=(100, 20), font_size=12, group=None, visible=True):
        default_style = {
            ControlState.DEFAULT: {
                "border_thickness": 1,
                "border_color": Basic.WHITE1,
                "background_color": Basic.WHITE_TINGE1,
            },
            ControlState.FOCUS: {
                "border_color": Basic.NEARWHITE,
            },
            ControlState.HOVER: {
                "border_color": Basic.NEARWHITE,
            },
            ControlState.DISABLED: {},
            ControlState.PRESSED: {}    # Unused in textbox
        }

        self._font_size = font_size
        self._original_height = size[1]
        self._prev_caret_mark = 0
        self._prev_caret_position = 0

        self._group_back = pyglet.graphics.OrderedGroup(0, group)
        self._group_front = pyglet.graphics.OrderedGroup(1, group)

        self.background = Rectangle(batch, position, size, group=self._group_back)
        self.border = [
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front),
            Line(batch, group=self._group_front)
        ]

        # Formatted document stores the formatting and text
        self._document = pyglet.text.document.FormattedDocument(' ')
        self._document.set_style(0, 1, dict(color=(0xCC, 0xCC, 0xCC, 0xff), font_name="Arimo", font_size=font_size))
        self._document.text = ''

        # IncrementalLayout handles displaying the document
        self._layout = pyglet.text.layout.IncrementalTextLayout(self._document, size[0] - 20, size[1],
                                                               wrap_lines=True, group=self._group_front,
                                                               multiline=True, batch=batch)
        self._layout.selection_color = Basic.NEARWHITE
        self._layout.selection_background_color = Basic.PRIMARY

        # Caret provides basic text entry functionality
        self._caret = pyglet.text.caret.Caret(self._layout, color=Basic.NEARWHITE[:3])
        self._caret.position = 0
        self._caret.mark = None
        self._caret.visible = False

        # Base class establishes style
        ControlElement.__init__(self, batch, default_style, group, position, size, visible)

        self._render()

    def get_text(self):
        return self._document.text

    def set_text(self, new_text):
        self._document.text = new_text
        self._render()

    def delete(self):
        self.background.delete()
        for line in self.border:
            line.delete()
        self._layout.delete()

    def _render(self):
        # Alter height based on line count
        line_count = self._layout.get_line_count()
        # lines = self._document.text.split('\n')
        self._size = self._size[0], self._original_height + (line_count - 1) * Textbox.BOX_LINE_HEIGHT
        self._layout.height = self._size[1]

        self._layout.x = self._position[0] + 10
        self._layout.y = UIElement.SCREEN_HEIGHT - self._position[1] - 8 - self._size[1]

        self.background.set_size(self._size)
        self.background.set_position(self._position)

        pos = self._position
        size = self._size
        self.border[0].set_points(pos, (pos[0] + size[0], pos[1]))
        self.border[1].set_points((pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] + size[1]))
        self.border[2].set_points((pos[0] + size[0], pos[1]), (pos[0] + size[0], pos[1] + size[1]))
        self.border[3].set_points((pos[0], pos[1] + size[1]), (pos[0] + size[0], pos[1] + size[1]))

    def alter_focus(self, flag):
        super().alter_focus(flag)
        self._caret.visible = flag

    def set_text_style(self, start, end, new_style: dict):
        self._document.set_style(start, end, new_style)

    def get_text_style(self, attr, start, end):
        return self._document.get_style_range(attr, start, end)

    def _update_caret(self):
        if self._prev_caret_mark != self._caret.mark or self._prev_caret_position != self._caret.position:
            self.dispatch_event('on_caret_change', self._caret.mark, self._caret.position)

        self._prev_caret_position = self._caret.position
        self._prev_caret_mark = self._caret.mark

    def handle_mouse_press(self, x, y, button, modifiers):
        if not self.is_point_within((x, y)):
            return

        if self._state != ControlState.FOCUS:
            self._caret.position = len(self._document.text)
        else:
            self._caret.on_mouse_press(x, y, button, modifiers)

        self._update_caret()

    def handle_key_press(self, symbol, modifiers):
        self.dispatch_event('on_key_press', symbol, modifiers)

        if symbol == key.A and modifiers & key.MOD_CTRL:
            self._caret.position = 0
            self._caret.mark = len(self._document.text)
            self._update_caret()

    def handle_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self._caret.on_mouse_drag(x, y, dx, dy, button, modifiers)
        self._update_caret()

    def handle_text(self, text):
        before = self._document.text
        self._caret.on_text(text)
        self._update_caret()
        self._render()

        if before != self._document.text:
            self.dispatch_event('on_text_change', self._document.text)

    def handle_text_motion(self, motion):
        before = self._document.text
        self._caret.on_text_motion(motion)
        self._update_caret()
        self._render()

        if before != self._document.text:
            self.dispatch_event('on_text_change', self._document.text)

    def handle_text_motion_select(self, motion):
        before = self._document.text
        self._caret.on_text_motion_select(motion)
        self._update_caret()
        self._render()

        if before != self._document.text:
            self.dispatch_event('on_text_change', self._document.text)

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


Textbox.register_event_type('on_text_change')
Textbox.register_event_type('on_caret_change')
Textbox.register_event_type('on_key_press')