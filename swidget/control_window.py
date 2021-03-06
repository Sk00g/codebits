import pyglet
from pyglet.window import key
from swidget import UIElement, ControlElement, ControlState



class ControlWindow(pyglet.window.Window):
    def __init__(self, width=640, height=480, caption='swidget window'):
        super().__init__(width, height, caption=caption)

        # Initialize swidget GUI framework
        UIElement.SCREEN_HEIGHT = height
        UIElement.SCREEN_WIDTH = width

        # Store all children, whether controls, panels, or simple elements
        self._children = []

        # Store control children for iteration, event-handling, and focus
        self._controls = []

        self._focus_index = -1
        self.order_controls()

    # Order the control children indexes based on Y position
    def order_controls(self):
        self._controls.sort(key=lambda ele: (ele.get_position()[1], ele.get_position()[0]))


    def add_children(self, *args):
        for child in args:
            if isinstance(child, list):
                for ch in child:
                    if ch in self._children:
                        raise Exception("Given element is already a child of ControlWindow!")

                    self._children.append(ch)

                    if isinstance(ch, ControlElement):
                        self._controls.append(ch)
                        self.push_handlers(
                            on_mouse_motion=ch.handle_mouse_motion,
                            on_mouse_drag=ch.handle_mouse_drag,
                            on_mouse_release=ch.handle_mouse_release,
                            on_mouse_press=ch.handle_mouse_press)
            else:
                if child in self._children:
                    raise Exception("Given element is already a child of ControlWindow!")

                self._children.append(child)

                if isinstance(child, ControlElement):
                    self._controls.append(child)
                    self.push_handlers(
                        on_mouse_motion=child.handle_mouse_motion,
                        on_mouse_drag=child.handle_mouse_drag,
                        on_mouse_release=child.handle_mouse_release,
                        on_mouse_press=child.handle_mouse_press
                    )

    def remove_children(self, *args):
        for child in args:
            if isinstance(child, list):
                for ch in child:
                    if ch in self._children:
                        self._children.remove(ch)
                        ch.delete()
                    if ch in self._controls:
                        self._controls.remove(ch)
            else:
                if child in self._children:
                    self._children.remove(child)
                    child.delete()
                if child in self._controls:
                    self._controls.remove(child)

    def on_mouse_press(self, x, y, button, modifiers):
        for control in self._controls:
            if control.is_point_within((x, y)) and control.get_state() != ControlState.DISABLED \
                    and control.is_tab_stop:
                if self._focus_index != -1:
                    self._controls[self._focus_index].alter_focus(False)

                self._focus_index = self._controls.index(control)
                self._controls[self._focus_index].alter_focus(True)


    def on_text(self, text):
        if self._focus_index != -1:
            self._controls[self._focus_index].handle_text(text)

    def on_text_motion(self, motion):
        if self._focus_index != -1:
            self._controls[self._focus_index].handle_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self._focus_index != -1:
            self._controls[self._focus_index].handle_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.TAB or symbol == 98784247808:
            self._handle_tab_press(modifiers)

        if symbol == key.ESCAPE:
            pyglet.app.exit()

        if self._focus_index != -1:
            self._controls[self._focus_index].handle_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if self._focus_index != -1:
            self._controls[self._focus_index].handle_key_release(symbol, modifiers)

    # --- Private Methods ---
    def _handle_tab_press(self, modifiers):
        if self._focus_index != -1:
            self._controls[self._focus_index].alter_focus(False)

        while True:
            self._focus_index += -1 if modifiers & key.MOD_SHIFT else 1
            if self._focus_index < 0:
                self._focus_index = len(self._controls) - 1
            if self._focus_index >= len(self._controls):
                self._focus_index = 0
            if self._controls[self._focus_index].is_tab_stop:
                break

        self._controls[self._focus_index].alter_focus(True)
