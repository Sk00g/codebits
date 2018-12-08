import pyglet
import re
from pyglet.window import key
from swidget import ControlWindow, Image, Rectangle, Label, Textbox, Button, Badge
from swidget.theme import Basic
from archive.const import *
from entry import EntryMaster
from model import DataEngine, Chunk, Codebit
from enums import *

FONT = 'Arimo'
WINDOW_CAPTION = 'Codebits'
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 427
WINDOW_SHADOW_COLOR = (10, 15, 25, 200)
MINIMUM_CODEBIT_SIZE = 4

CHUNK_COLORS = {
    ChunkType.PLAIN_TEXT: [0, 0, 0, 0],
    ChunkType.CREDENTIALS: Basic.PRIMARY_LIGHT_TINGE,
    ChunkType.PHONE_NUMBER: Basic.PRIMARY_LIGHT_TINGE,
    ChunkType.ADDRESS: Basic.PRIMARY_LIGHT_TINGE,
    ChunkType.CLI: Basic.PRIMARY_LIGHT_TINGE,
    ChunkType.CODE: Basic.PRIMARY_LIGHT_TINGE,
    ChunkType.DATE: Basic.PRIMARY_LIGHT_TINGE,
    ChunkType.LINK: Basic.PRIMARY_LIGHT_TINGE,
    ChunkType.QUOTE: Basic.PRIMARY_LIGHT_TINGE,
    ChunkType.TIME: Basic.PRIMARY_LIGHT_TINGE
}


class MainWindow(ControlWindow):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, caption=WINDOW_CAPTION)

        self.ctype = CodebitType.CHILL
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
        self.textbox.push_handlers(
            on_text_change=self.on_textbox_change,
            on_caret_change=self.on_textbox_caret_change
        )
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

        # Status strings
        self.ctype_label = Label(self.batch, position=(15, 15), text="type: CHILL", group=self.group_front, font_size=10)
        self.chunk_count_label = Label(self.batch, position=(15, 35), text="chunks: 0", group=self.group_front, font_size=10)
        self.char_count_label = Label(self.batch, position=(15, 55), text="chars: 0", group=self.group_front, font_size=10)
        self.add_children(self.ctype_label, self.chunk_count_label, self.char_count_label)

        self.order_controls()

        self.entry_master = EntryMaster(self.textbox)
        self.entry_master.push_handlers(
            on_add_chunk=self.on_chunk_add,
            on_add_topic=self.on_topic_add,
            on_codebit_type_change=self.on_codebit_type_change
        )
        self.engine = DataEngine()

    # --- HELPERS ---
    def _all_string_indices(self, string, sub):
        indices = []
        i = string.find(sub)
        while i >= 0:
            indices.append(i)
            i = string.find(sub, i + 1)
        return indices

    def on_codebit_type_change(self, new_type):
        print('changed codebit type to %s' % new_type)
        self.ctype = new_type
        self._update_status_labels()

    def on_chunk_add(self, chunk_type, start, end):
        print('add chunk request for (%s, %s)' % (chunk_type, self.textbox.get_text()[start:end]))
        self.chunks.append(Chunk(None, chunk_type, start, end))
        self._update_status_labels()

    def on_topic_add(self, start, end):
        print('add topic request for (%s)' % (self.textbox.get_text()[start:end]))
        text = self.textbox.get_text()[start:end]
        if text in self.topics:
            self.topics.remove(text)
        else:
            self.topics.append(text)
        self.update_topics()

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

    def on_textbox_caret_change(self, mark, position):
        pass

    def _update_status_labels(self):
        self.ctype_label.set_text("type: %s" % self.ctype)
        self.chunk_count_label.set_text("chunks: %d" % len(self.chunks))
        self.char_count_label.set_text("chars: %d" % len(self.textbox.get_text()))

    def on_textbox_change(self, text):
        self._update_status_labels()

        # Clear text styling
        self.textbox.set_text_style(0, len(text), dict(color=Basic.OFFWHITE, background_color=None))

        # Update topic styles
        for topic in self.topics:
            index_list = self._all_string_indices(text, topic)
            if index_list:
                for index in index_list:
                    self.textbox.set_text_style(index, index + len(topic), dict(color=Basic.PRIMARY_HIGHLIGHT))

        # Update chunk styles
        for chunk in self.chunks:
            self.textbox.set_text_style(chunk.start, chunk.end,
                                        dict(color=Basic.NEARWHITE, background_color=CHUNK_COLORS[chunk.ctype]))

        # Update codebit type




    def on_draw(self):
        self.clear()
        self.batch.draw()