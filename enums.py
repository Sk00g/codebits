
"""
These enumerations should map directly to the MySQL backend
"""

from pyglet.window import key


class ChunkType:
    PLAIN_TEXT = "Plain Text"
    QUOTE = "Quote"
    PHONE_NUMBER = "Phone Number"
    CODE = "Code"
    CLI = "CLI"
    CREDENTIALS = "Credentials"
    LINK = "Link"
    DATE = "Date"
    TIME = "Time"
    ADDRESS = "Address"

class CodebitType:
    CHILL = "Chill"
    IMPORTANT = "Important"
    REMINDER = "Reminder"

class EntryMode:
    BASIC = "Basic"
    CHUNK = "Chunk"
    TOPIC = "Topic"

TOPIC_HOTKEY = key.T

CODEBIT_HOTKEYS = {
    key._1: CodebitType.CHILL,
    key._2: CodebitType.IMPORTANT,
    key._3: CodebitType.REMINDER,
    key.NUM_1: CodebitType.CHILL,
    key.NUM_2: CodebitType.IMPORTANT,
    key.NUM_3: CodebitType.REMINDER
}

CHUNK_HOTKEYS = {
    key.Q: ChunkType.QUOTE,
    key.P: ChunkType.PHONE_NUMBER,
    key.BRACKETLEFT: ChunkType.CODE,
    key.MINUS: ChunkType.CLI,
    key.R: ChunkType.CREDENTIALS,
    key.L: ChunkType.LINK,
    key.D: ChunkType.DATE,
    key.I: ChunkType.TIME,
    key.S: ChunkType.ADDRESS
}