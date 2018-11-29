from model import Chunk
from enums import *


class Codebit:
    def __init__(self, content: str, chunks: list, topics: list, codebit_type=CodebitType.CHILL):
        self.ctype = codebit_type
        self.content = content
        self.chunks = chunks
        self.topics = topics




