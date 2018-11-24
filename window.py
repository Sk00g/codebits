import pyglet
from pyglet.window import key
from swidget import ControlWindow, UIElement, Image, Rectangle, Label, Textbox
from const import *


FONT = 'Arimo'
WINDOW_CAPTION = 'Codebits'
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 427
WINDOW_SHADOW_COLOR = (10, 15, 25, 200)

class MainWindow(ControlWindow):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, caption=WINDOW_CAPTION)

        self.mode = Mode.ENTER

        # Use a single batch with foreground / background groups to draw everything for now
        self.batch = pyglet.graphics.Batch()
        self.group_bkgr = pyglet.graphics.OrderedGroup(0)
        self.group_back = pyglet.graphics.OrderedGroup(1)
        self.group_front = pyglet.graphics.OrderedGroup(2)

        self.background = Image(self.batch, 'assets/pexels-photo-242236.jpeg', group=self.group_bkgr)
        self.background_shadow = Rectangle(self.batch, size=(WINDOW_WIDTH, WINDOW_HEIGHT), color=WINDOW_SHADOW_COLOR, group=self.group_back)
        self.add_children(self.background, self.background_shadow)

        # Title
        self.title = Label(self.batch, text='codebits', font_name="Arimo", font_size=18, font_color=(0xDD, 0xDD, 0xDD, 0xff),
                           group=self.group_front)
        self.title.center(WINDOW_WIDTH // 2, 50)
        self.add_children(self.title)

        # Textbox
        self.textbox = Textbox(self.batch, size=(500, 34), font_size=12, group=self.group_front)
        self.textbox.center(WINDOW_WIDTH // 2, 300)
        self.textbox.push_handlers(on_hover=self.textbox_hovered)
        self.add_children(self.textbox)

        self.textbox2 = Textbox(self.batch, size=(500, 34), font_size=12, group=self.group_front)
        self.textbox2.center(WINDOW_WIDTH // 2, 130)
        self.add_children(self.textbox2)

        self.order_controls()

        # Button icons
        # self.search_icon = pyglet.resource.image('assets/search2-purple.png')
        # self.enter_icon = pyglet.resource.image('assets/login2-teal.png')
        #
        # # Title
        # self.title = pyglet.text.Label(TITLE_TEXT, FONT, TITLE_SIZE, x=self.width // 2, y=TITLE_Y,
        #                                anchor_x='center', anchor_y='center', color=TITLE_COLOR)
        #
        # # Text box
        # self.box = TextBox(self, self.batch, (WINDOW_WIDTH // 2 - (BOX_WIDTH + BUTTON_WIDTH) // 2, BOX_Y),
        #                    (BOX_WIDTH, BOX_HEIGHT), BOX_BORDER_DEFAULT, (255, 255, 255, 10))
        # self.box.hover_border_color = BOX_BORDER_HOVER
        #
        # # Button
        # self.mode_button = Button(self.batch, self.search_icon, (self.box.location[0] + self.box.size[0], self.box.location[1]),
        #                             (BUTTON_WIDTH, BUTTON_HEIGHT), BUTTON_BKGR_DEFAULT, BUTTON_BORDER_DEFAULT)
        # self.mode_button.hover_bkgr = BUTTON_BKGR_HOVER[self.mode]
        # self.mode_button.hover_border = BUTTON_BORDER_HOVER
        # self.mode_button.click_actions.append(self._change_mode)
        #
        # # Lists for simplified handling of input events
        # self.mouse_motion_controls = [self.box, self.mode_button]
        # self.mouse_click_controls = [self.box, self.mode_button]
        # self.keyboard_controls = [self.box, self.mode_button]
        #
        # # Import to add focusable controls in the order you want to tab through them
        # self.focusable_controls = [self.box, self.mode_button]
        #
        # # test
        # self.test_badge = Badge((100, 100), 'Infiniti', CT_PRIMARY[Mode.SEARCH], CT_PRIMARY_LIGHT_TINGE[Mode.SEARCH])
        # self.test_badge2 = Badge((200, 100), 'Work', CT_PRIMARY[Mode.ENTER], CT_PRIMARY_LIGHT_TINGE[Mode.ENTER])

    def textbox_hovered(self):
        print("textbox is hovered, raise tooltip")

    def _change_mode(self):
        if self.mode == Mode.ENTER:
            self.mode = Mode.SEARCH
        elif self.mode == Mode.SEARCH:
            self.mode = Mode.ENTER

    # def on_key_press(self, symbol, modifiers):
    #     if symbol == key.A:
    #         old = self.textbox.get_position()
    #         self.textbox.set_position((old[0] - 5, old[1] - 5))
    #     elif symbol == key.S:
    #         old = self.textbox.get_position()
    #         self.textbox.set_position((old[0] + 5, old[1] + 5))
    #
    #     if symbol == key.ESCAPE:
    #         self.close()


    #
    # def _update_focus(self):
    #     for i in range(len(self.focusable_controls)):
    #         self.focusable_controls[i].alter_focus(i == self.focused_control_index)
    #
    # def on_mouse_motion(self, x, y, dx, dy):
    #     for control in self.mouse_click_controls:
    #         control.handle_mouse_motion(x, y)
    #
    # def on_mouse_press(self, x, y, button, modifiers):
    #     print('mouse was pressed at %d, %d with button %s || (%s)' % (x, y, button, modifiers))
    #
    #     for control in self.mouse_click_controls:
    #         if control.handle_mouse_press(x, y, button, modifiers):
    #             self.focused_control_index = self.focusable_controls.index(control)
    #             self._update_focus()
    #
    # def on_mouse_release(self, x, y, button, modifiers):
    #     for control in self.mouse_click_controls:
    #         control.handle_mouse_release(x, y, button, modifiers)
    #
    # def on_key_press(self, symbol, modifiers):
    #     # Tab or Shift + Tab presses iterate through focusable controls
    #     if symbol == key.TAB:
    #         self.focused_control_index += -1 if modifiers & key.MOD_SHIFT else 1
    #         if self.focused_control_index < 0:
    #             self.focused_control_index = len(self.focusable_controls) - 1
    #         elif self.focused_control_index == len(self.focusable_controls):
    #             self.focused_control_index = 0
    #         self._update_focus()
    #
    #     if symbol == key.ESCAPE:
    #         self.close()
    #
    #     for control in self.keyboard_controls:
    #         control.handle_key_press(symbol, modifiers)
    #
    # def on_key_release(self, symbol, modifiers):
    #     for control in self.keyboard_controls:
    #         control.handle_key_release(symbol, modifiers)
    #
    # # Pass these along only to the text box
    # def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    #     self.box.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    #
    # def on_text(self, text):
    #     self.box.on_text(text)
    #
    # def on_text_motion(self, motion):
    #     self.box.on_text_motion(motion)
    #
    # def on_text_motion_select(self, motion):
    #     self.box.on_text_motion_select(motion)
    #
    # def on_textbox_update(self):
    #     # Update the list of topic badges
    #     #
    #     pass


    def on_draw(self):
        self.clear()
        self.batch.draw()
