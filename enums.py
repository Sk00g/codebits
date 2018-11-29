
"""
These enumerations should map directly to the MySQL backend
"""

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

class TECommand:
    TOPIC = "T"
    CREDENTIAL = "C"
    PHONE = "P"
    CLI = "L"
    ADDRESS = "A"
    REMINDER = "R"
    CHILL = "H"
    IMPORTANT = "I"

CHUNK_TYPE = {
    TECommand.ADDRESS: ChunkType.ADDRESS,
    TECommand.CREDENTIAL: ChunkType.CREDENTIALS,
    TECommand.PHONE: ChunkType.PHONE_NUMBER,
    TECommand.CLI: ChunkType.CLI,
}