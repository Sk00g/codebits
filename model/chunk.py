from enums import *


class Chunk:
    def __init__(self, host, chunk_type: str, start: int, end: int):
        self.host = host
        self.ctype = chunk_type
        self.start = start
        self.end = end





