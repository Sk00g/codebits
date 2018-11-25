
"""
These enumerations should map directly to the MySQL backend
"""

class Chunk:
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