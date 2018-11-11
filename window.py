import pyglet
from primitives import Rectangle, Line
from elements.textbox import TextBox
from elements.button import Button
from const import *


class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, caption=WINDOW_CAPTION)

        # Use a single batch to draw everything for now
        self.batch = pyglet.graphics.Batch()

        # Background
        self.background = pyglet.resource.image('assets/pexels-photo-242236.jpeg')
        self.background_shadow = Rectangle(self.batch, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_SHADOW_COLOR)

        # Button icons
        self.search_icon = pyglet.resource.image('assets/search-purple.png')
        self.enter_icon = pyglet.resource.image('assets/login-teal.png')

        # Title
        self.title = pyglet.text.Label(TITLE_TEXT, FONT, TITLE_SIZE, x=self.width // 2, y=TITLE_Y,
                                       anchor_x='center', anchor_y='center', batch=self.batch, color=TITLE_COLOR)

        # Text box
        self.box = TextBox(self.batch, (WINDOW_WIDTH // 2 - (BOX_WIDTH + BUTTON_WIDTH) // 2, BOX_Y),
                           (BOX_WIDTH, BOX_HEIGHT), BOX_BORDER_DEFAULT, 1, (255, 255, 255, 10))
        self.box.hover_border_color = BOX_BORDER_HOVER

        # Button
        self.mode_button = Button(self.batch, self.search_icon, (self.box.location[0] + self.box.size[0], self.box.location[1]),
                                    (BUTTON_WIDTH, BUTTON_HEIGHT), BUTTON_BKGR_DEFAULT, BUTTON_BORDER_DEFAULT)
        self.mode_button.hover_bkgr = BUTTON_BKGR_HOVER['search']
        self.mode_button.hover_border = BUTTON_BORDER_HOVER

        # While testing
        self._test()

    def _test(self):
        # rect = Rectangle(self.batch, 100, 100, 200, 200, (0, 0, 0, 100))
        # line = Line(self.batch, (10, 10), (110, 10), 11, (0, 255, 0, 255))
        # self.box = TextBox(self.batch, (WINDOW_WIDTH // 2 - BOX_WIDTH // 2, BOX_Y),
        #               (BOX_WIDTH, BOX_HEIGHT), BOX_BORDER_DEFAULT['search'], 1, (255, 255, 255, 10))
        # self.box.hover_border_color = BOX_BORDER_HOVER['search']
        return

    def on_mouse_motion(self, x, y, dx, dy):
        self.mode_button.handle_mouse(x, y)

        if self.box.handle_mouse(x, y):
            self.set_mouse_cursor(self.get_system_mouse_cursor('text'))
        else:
            self.set_mouse_cursor(self.get_system_mouse_cursor(pyglet.window.Window.CURSOR_DEFAULT))

    def on_mouse_press(self, x, y, button, modifiers):
        self.mode_button.handle_mouse_press(x, y)
        self.box.handle_mouse_press(x, y, button, modifiers)

    def on_draw(self):
        self.clear()
        self.background.blit(0, 0)
        self.batch.draw()