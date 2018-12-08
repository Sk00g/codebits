import pyglet
from pyglet.window import key
from swidget import ControlWindow, Image, Rectangle, Label, Textbox, Button, Badge
from swidget.theme import Basic
from archive.const import *
from entry import EntryMaster
from model import DataEngine

FONT = 'Arimo'
WINDOW_CAPTION = 'Codebits'
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 427
WINDOW_SHADOW_COLOR = (10, 15, 25, 200)
MINIMUM_CODEBIT_SIZE = 4


class MainWindow(ControlWindow):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, caption=WINDOW_CAPTION)

        self.topics = []
        self.topic_badges = []
        self.chunks = []

        # Use a single batch with foreground / background groups to draw everything for now
        self.batch = pyglet.graphics.Batch()
        self.group_bkgr = pyglet.graphics.OrderedGroup(0)
        self.group_back = pyglet.graphics.OrderedGroup(1)
        self.group_front = pyglet.graphics.OrderedGroup(2)

        self.background = Image(self.batch, 'assets/pexels-photo-242236.jpeg', group=self.group_bkgr)
        self.background_shadow = Rectangle(self.batch, size=(WINDOW_WIDTH, WINDOW_HEIGHT), color=WINDOW_SHADOW_COLOR, group=self.group_back)
        self.add_children(self.background, self.background_shadow)

        # Title
        self.title = Label(self.batch, text='codebits', font_name="Arimo", font_size=18, font_color=Basic.OFFWHITE,
                           group=self.group_front)
        self.title.center(WINDOW_WIDTH // 2, 50)
        self.add_children(self.title)

        # Textbox
        self.textbox = Textbox(self.batch, size=(500, 34), font_size=12, group=self.group_front)
        self.textbox.center(WINDOW_WIDTH // 2, 130)
        self.textbox.push_handlers(on_text_change=self.on_textbox_change)
        self.add_children(self.textbox)

        # Mode Button
        self.search_button = Button(self.batch, 'assets/search2-purple.png',
                                  (self.textbox.get_position()[0] - 34, self.textbox.get_position()[1]),
                                  (34, 34), lambda: print('clicked search'), self.group_front)

        # Enter button
        self.enter_button = Button(self.batch, 'assets/login2-teal.png',
                                   (self.textbox.get_position()[0] + self.textbox.get_size()[0], self.textbox.get_position()[1]),
                                   (34, 34), group=self.group_front)
        self.add_children(self.search_button, self.enter_button)

        self.order_controls()

        self.entry_master = EntryMaster(self.textbox)
        self.entry_master.push_handlers(
            on_add_chunk=self.on_chunk_add,
            on_add_topic=self.on_topic_add,
            on_codebit_type_change=self.on_codebit_type_change
        )
        self.engine = DataEngine()

    def on_codebit_type_change(self, new_type):
        print('changed codebit type to %s' % new_type)

    def on_chunk_add(self, chunk_type, start, end):
        print('add chunk request for (%s, %s)' % (chunk_type, self.textbox.get_text()[start:end]))

    def on_topic_add(self, start, end):
        print('add topic request for (%s)' % (self.textbox.get_text()[start:end]))

    def badge_click(self, badge):
        print('clicked badge %s' % badge)

    def update_topics(self):
        if self.topic_badges:
            self.remove_children(self.topic_badges)
            self.topic_badges.clear()

        totalx = 0
        for id in range(len(self.topics)):
            topic = self.topics[id]

            position = self.textbox.left() + totalx + id * 10, self.textbox.bottom() + 12
            modulo = id % 4
            if modulo == 0:
                border, tinge = Basic.PRIMARY, Basic.PRIMARY_BRIGHT_TINGE
            elif modulo == 1:
                border, tinge = Basic.SECOND, Basic.SECOND_BRIGHT_TINGE
            elif modulo == 2:
                border, tinge = Basic.THIRD, Basic.THIRD_BRIGHT_TINGE
            else:
                border, tinge = Basic.FOURTH, Basic.FOURTH_BRIGHT_TINGE
            style = {
                ControlState.DEFAULT: dict(border_color=border),
                ControlState.HOVER: dict(background_color=tinge)
            }

            badge = Badge(self.batch, text=topic, click_event=lambda: self.badge_click(badge),
                          position=position, group=self.group_front)
            badge.update_style(style)
            self.topic_badges.append(badge)
            totalx += badge.get_size()[0]

        if self.topic_badges:
            self.add_children(self.topic_badges)

    def submit_codebit(self):
        if len(self.textbox.get_text()) < MINIMUM_CODEBIT_SIZE:
            # popup with error??
            return

        # codebit_data = self.templater.generate_snapshot()
        # self.engine.insert_codebit(codebit_data)

        self.textbox.set_text("")
        self.on_textbox_change("")
        self.topics = []
        self.update_topics()

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)

        if self._focus_index == self._controls.index(self.textbox) and symbol == key.ENTER and modifiers & key.MOD_CTRL:
            self.submit_codebit()

    def on_textbox_change(self, text):
        pass
        # response = self.templater.parse_input(text)
        #
        # # Match text to templater output
        # if response['altered_text'] != text:
        #     text = response['altered_text']
        #     old_position = self.textbox._caret.position
        #     self.textbox.set_text(text)
        #     self.textbox._caret.position = len(text)
        #
        # # Clear text styling
        # self.textbox.set_text_style(0, len(text), dict(color=Basic.OFFWHITE, background_color=None))
        #
        # # Highlight partial commands
        # if response['partial_command']:
        #     start, end = response['partial_command']
        #     self.textbox.set_text_style(start, end, dict(background_color=Basic.PRIMARY_LIGHT_TINGE))
        #
        # # Update topics ok
        # if response['new_topics']:
        #     self.topics.extend(response['new_topics'])
        # if response['removed_topics']:
        #     for topic in response['removed_topics']:
        #         self.topics.remove(topic)
        # if response['new_topics'] or response['removed_topics']:
        #     self.update_topics()

        # Update chunk styles

        # Update codebit type


    def on_draw(self):
        self.clear()
        self.batch.draw()