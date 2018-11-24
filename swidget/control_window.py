import pyglet
from pyglet.window import key
from swidget import UIElement, ControlElement



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
        self._controls.sort(key=lambda ele: ele.get_position()[1])

    def add_children(self, *args):
        for child in args:
            if child in self._children:
                raise Exception("Given element is already a child of ControlWindow!")

            self._children.append(child)

            if isinstance(child, ControlElement):
                self._controls.append(child)

    def on_mouse_motion(self, x, y, dx, dy):
        for control in self._controls:
            control.handle_mouse_motion(x, y)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.TAB or symbol == 98784247808:
            self._handle_tab_press(modifiers)

        if symbol == key.ESCAPE:
            pyglet.app.exit()


    # --- Private Methods ---
    def _handle_tab_press(self, modifiers):
        if self._focus_index != -1:
            self._controls[self._focus_index].alter_focus(False)

        if modifiers & key.MOD_SHIFT:
            self._focus_index -= 1
            if self._focus_index < 0:
                self._focus_index = len(self._controls) - 1
        else:
            self._focus_index += 1
            if self._focus_index >= len(self._controls):
                self._focus_index = 0

        self._controls[self._focus_index].alter_focus(True)