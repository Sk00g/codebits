import pyglet
from swidget import UIElement, ControlState


class ControlElement(UIElement):
    def __init__(self, batch, style: dict={}, group=None, position=(0, 0), size=(0, 0), visible=True, is_tab_stop=True):
        UIElement.__init__(self, batch, group, position, size, visible)

        self._style = {}
        self._state = ControlState.DEFAULT
        self._has_focus = False

        self.is_tab_stop = is_tab_stop

        self.update_style(style)

    def _update_state(self, new_state):
        if self._state == new_state:
            return

        self._state = new_state
        self._apply_style()

    # --- Public Methods ---

    """
    Pass in a dictionary of objects in the pattern:
        state1: { 
            {prop1: value1 }, 
            {prop2: value2 },
            etc..
        }
        state2: {
            etc...
    """
    def update_style(self, style_update: dict):
        for state in style_update:
            if state not in self._style:
                self._style[state] = {}

            for prop in style_update[state]:
                self._style[state][prop] = style_update[state][prop]

        self._apply_style()

    def get_style(self, state, prop):
        return self._style[state][prop]

    # --- Abstract Methods ---

    """
    Child-specific method called whenever state changes or style property is updated.
    Will parse through the 'self._style' dictionary member and apply values as appropriate to its own appearance
    Which value is used for each property is dependent on what state the control element is currently in
    """
    def _apply_style(self):
        raise NotImplementedError()

    """
    Alter focus directly, typically called by ControlWindow parent
    This method also affects state and subsequently style
    """
    def alter_focus(self, flag):
        if flag:
            if self._state != ControlState.FOCUS:
                self._update_state(ControlState.FOCUS)
            self._has_focus = True
        else:
            if self._state == ControlState.FOCUS:
                self._update_state(ControlState.DEFAULT)
            self._has_focus = False

    """
    Handle different events, dished here by a parent ControlWindow object.
    Feel free to override these, otherwise the most obvious base functionality is provided here.
    """
    def handle_mouse_motion(self, x, y):
        if (0 < x - self._position[0] < self._size[0] and
                0 < (UIElement.SCREEN_HEIGHT - y) - self._position[1] < self._size[1]):
            # Only change to hover state if we are in DEFAULT
            if self._state == ControlState.DEFAULT or self._state == ControlState.FOCUS:
                self._update_state(ControlState.HOVER)
        else:
            # Only change back from hover state if mouse leaves
            if self._state == ControlState.HOVER:
                self._update_state(ControlState.FOCUS if self._has_focus else ControlState.DEFAULT)
