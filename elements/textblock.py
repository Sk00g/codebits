from typing import Tuple


class TextBlock:
    def __init__(self, text: str, color: Tuple[int, int, int, int], locx: int, locy: int):
        self.text = text
        self.base_color = color
        self.sections = []
        self.location = (locx, locy)

    def set_color(self, new_color: Tuple[int, int, int, int]):
        pass

    def alter_section(self, start_index: int, end_index: int, new_color: Tuple[int, int, int, int],
                      new_size: int, new_highlight: Tuple[int, int, int, int]):
        pass