import pyglet
from pyglet.window import key
from primitives import Rectangle, Line
from elements.textbox import TextBox
from elements.button import Button
from const import *



class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, caption=WINDOW_CAPTION)

        self.mode = Mode.ENTER
        self.focused_control_index = -1

        # Use a single batch to draw everything for now
        self.batch = pyglet.graphics.Batch()

        # Background
        self.background = pyglet.resource.image('assets/pexels-photo-242236.jpeg')
        self.background_shadow = Rectangle(self.batch, None, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_SHADOW_COLOR)

        # Button icons
        self.search_icon = pyglet.resource.image('assets/search2-purple.png')
        self.enter_icon = pyglet.resource.image('assets/login2-teal.png')

        # Title
        self.title = pyglet.text.Label(TITLE_TEXT, FONT, TITLE_SIZE, x=self.width // 2, y=TITLE_Y,
                                       anchor_x='center', anchor_y='center', color=TITLE_COLOR)

        # Text box
        self.box = TextBox(self, self.batch, (WINDOW_WIDTH // 2 - (BOX_WIDTH + BUTTON_WIDTH) // 2, BOX_Y),
                           (BOX_WIDTH, BOX_HEIGHT), BOX_BORDER_DEFAULT, (255, 255, 255, 10))
        self.box.hover_border_color = BOX_BORDER_HOVER

        # Button
        self.mode_button = Button(self.batch, self.search_icon, (self.box.location[0] + self.box.size[0], self.box.location[1]),
                                    (BUTTON_WIDTH, BUTTON_HEIGHT), BUTTON_BKGR_DEFAULT, BUTTON_BORDER_DEFAULT)
        self.mode_button.hover_bkgr = BUTTON_BKGR_HOVER[self.mode]
        self.mode_button.hover_border = BUTTON_BORDER_HOVER
        self.mode_button.click_actions.append(self._change_mode)

        # Lists for simplified handling of input events
        self.mouse_motion_controls = [self.box, self.mode_button]
        self.mouse_click_controls = [self.box, self.mode_button]
        self.keyboard_controls = [self.box, self.mode_button]

        # Import to add focusable controls in the order you want to tab through them
        self.focusable_controls = [self.box, self.mode_button]


    def _change_mode(self):
        if self.mode == Mode.ENTER:
            self.mode = Mode.SEARCH
            self.mode_button.set_icon(self.search_icon)
        elif self.mode == Mode.SEARCH:
            self.mode = Mode.ENTER
            self.mode_button.set_icon(self.enter_icon)

    def _update_focus(self):
        for i in range(len(self.focusable_controls)):
            self.focusable_controls[i].alter_focus(i == self.focused_control_index)

    def on_mouse_motion(self, x, y, dx, dy):
        for control in self.mouse_click_controls:
            control.handle_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        print('mouse was pressed at %d, %d with button %s || (%s)' % (x, y, button, modifiers))

        for control in self.mouse_click_controls:
            if control.handle_mouse_press(x, y, button, modifiers):
                self.focused_control_index = self.focusable_controls.index(control)
                self._update_focus()

    def on_mouse_release(self, x, y, button, modifiers):
        for control in self.mouse_click_controls:
            control.handle_mouse_release(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        # Tab or Shift + Tab presses iterate through focusable controls
        if symbol == key.TAB:
            self.focused_control_index += -1 if modifiers & key.MOD_SHIFT else 1
            if self.focused_control_index < 0:
                self.focused_control_index = len(self.focusable_controls) - 1
            elif self.focused_control_index == len(self.focusable_controls):
                self.focused_control_index = 0
            self._update_focus()

        if symbol == key.ESCAPE:
            self.close()

        for control in self.keyboard_controls:
            control.handle_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        for control in self.keyboard_controls:
            control.handle_key_release(symbol, modifiers)

    # Pass these along only to the text box
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.box.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        self.box.on_text(text)

    def on_text_motion(self, motion):
        self.box.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        self.box.on_text_motion_select(motion)


    def on_draw(self):
        self.clear()
        self.background.blit(0, 0)
        self.batch.draw()
        self.title.draw()
