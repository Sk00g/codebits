import pyglet
from enums import *
from swidget import Textbox

WHITESPACE = [' ', '\n', '\t']

class EntryMaster(pyglet.event.EventDispatcher):
    def __init__(self, host: Textbox):
        self.host = host
        host.push_handlers(
            on_text_change=self.handle_text_change,
            on_key_press=self.handle_key_press,
            on_caret_change=self.handle_caret_change
        )

        # --- Public Properties ---

        self.mode = EntryMode.BASIC

        # Keep track of entry mode progress
        self.mode_start = 0

        # Type of chunk data being entered when in EntryMode.CHUNK
        self.chunk_data_type = ChunkType.PLAIN_TEXT

        # Keep track of current selection and word for simplicity
        self.selection = None
        self.word = None

    def _reset_mode(self):
        self.mode = EntryMode.BASIC
        self.chunk_data_type = ChunkType.PLAIN_TEXT
        print('reset mode')

    def _get_word_text(self):
        return self.host.get_text()[self.word[0]:self.word[1]]

    def _find_word(self, text, position):
        index, start = position - 1, 0
        while index > 0 and not text[index] in WHITESPACE:
            index -= 1

        # Edge case of being at position 0
        if index == -1:
            index = 0

        start = index if text[index] not in WHITESPACE else index + 1
        index += 1
        while index != len(text) and not text[index] in WHITESPACE:
            index += 1
        self.word = (start, index) if start != index else None

    def handle_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self._reset_mode()
            return

        if symbol in [key.SPACE] and self.mode == EntryMode.TOPIC:
            self.dispatch_event('on_add_topic', self.mode_start, self.host._caret.position)
            self._reset_mode()
            return

        if modifiers & key.MOD_SHIFT:
            if symbol == key.ENTER and self.mode == EntryMode.CHUNK:
                if self.host._caret.position > self.mode_start:
                    self.dispatch_event('on_add_chunk', self.chunk_data_type, self.mode_start, self.host._caret.position)
                    self._reset_mode()

        if modifiers & key.MOD_CTRL:
            if symbol == key.BACKSPACE:
                self._reset_mode()
                return

            for hkey in CODEBIT_HOTKEYS:
                if symbol == hkey:
                    self.dispatch_event('on_codebit_type_change', CODEBIT_HOTKEYS[hkey])

            if symbol == TOPIC_HOTKEY:
                if self.mode == EntryMode.TOPIC:
                    self._reset_mode()

                elif not self.selection and not self.word:
                    self.mode = EntryMode.TOPIC
                    self.mode_start = self.host._caret.position
                    print('entering topic mode')

                elif self.word:
                    self.dispatch_event('on_add_topic', self.word[0], self.word[1])
                    self._reset_mode()

            if symbol in CHUNK_HOTKEYS.keys():
                selected_mode = CHUNK_HOTKEYS[symbol]
                # If chosen mode is already selected, escape chunk mode
                if self.mode == EntryMode.CHUNK and selected_mode == self.chunk_data_type:
                    self._reset_mode()

                # If we have selected and alternate chunk while in entry mode, swap type
                elif self.mode == EntryMode.CHUNK or self.mode == EntryMode.TOPIC:
                    self.chunk_data_type = selected_mode
                    print('swapped modes to %s' % selected_mode)

                # If there is no selection and we are within whitespace or EOL, start entry mode
                elif not self.selection and not self.word:
                    self.mode = EntryMode.CHUNK
                    self.chunk_data_type = selected_mode
                    self.mode_start = self.host._caret.position
                    print('entering chunk mode: %s' % selected_mode)

                # If we have selection or containing word, make that a chunk
                elif self.selection:
                    mark, position = self.host._caret.mark, self.host._caret.position
                    self.dispatch_event('on_add_chunk', selected_mode, min(mark, position), max(mark, position))
                    self._reset_mode()

                # No selection but caret is within a word
                elif self.word:
                    self.dispatch_event('on_add_chunk', selected_mode, self.word[0], self.word[1])
                    self._reset_mode()


    def handle_text_change(self, text):
        pass

    def handle_caret_change(self, mark, position):
        if len(self.host.get_text()) < 2:
            return

        # print('mark: %s | position: %s' % (mark, position))
        if mark:
            self.word = None
            self.selection = self.host.get_text()[min(mark, position):max(mark, position)]
            # print('selected text: %s' % self.selection)
        else:
            self.selection = None
            self._find_word(self.host.get_text(), position)
            # if self._word and self._get_word_text() != ' ':
                # print('containing word: %s' % self._get_word_text())

        if self.mode in [EntryMode.CHUNK, EntryMode.TOPIC] and position < self.mode_start:
            self._reset_mode()


# (ChunkType.*, start, end)
EntryMaster.register_event_type('on_add_chunk')

# (start, end))
EntryMaster.register_event_type('on_add_topic')

# (CodebitType.*)
EntryMaster.register_event_type('on_codebit_type_change')