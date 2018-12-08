import pyglet
from enums import *
from swidget import Textbox


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

        # Text that has been entered since the recent mode switch
        self.mode_text = ""

        # Type of chunk data being entered when in EntryMode.CHUNK
        self.chunk_data_type = ChunkType.PLAIN_TEXT


    def handle_key_press(self, symbol, modifiers):
        if modifiers & key.MOD_CTRL:
            for hkey in CODEBIT_HOTKEYS:
                if symbol == hkey:
                    self.dispatch_event('on_codebit_type_change', CODEBIT_HOTKEYS[hkey])

            for hkey in CHUNK_HOTKEYS:


    def handle_text_change(self, text):
        print('text change')

    def handle_caret_change(self, mark, position):
        print('caret change')

# (ChunkType.*, start, end)
EntryMaster.register_event_type('on_add_chunk')

# (start, end, remove: bool))
EntryMaster.register_event_type('on_add_topic')

# (CodebitType.*)
EntryMaster.register_event_type('on_codebit_type_change')