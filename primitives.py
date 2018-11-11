import pyglet
from typing import Tuple

class Rectangle(object):
    def __init__(self, batch, group, left, top, right, bottom, color: Tuple[int, int, int, int]):
        self._batch = batch
        self._color = color
        self._left = left
        self._right = right
        self._top = top
        self._bottom = bottom
        self.vertex_list = None
        self.group = group

        self._build_vertex_list()

    def _build_vertex_list(self):
        if self.vertex_list:
            self.vertex_list.delete()

        self.vertex_list = self._batch.add(
            4, pyglet.gl.GL_QUADS, self.group,
             ('v2i', [self._left, self._top, self._right, self._top, self._right, self._bottom, self._left, self._bottom]),
             ('c4B', self._color * 4)
        )

    def delete(self):
        if self.vertex_list:
            self.vertex_list.delete()

    def get_color(self):
        return self._color

    def set_color(self, new_color):
        self._color = new_color
        self._build_vertex_list()

    def get_size(self):
        return self._right - self._left, self._top - self._bottom

    def set_size(self, new_size):
        self._right = self._left + new_size[0]
        self._bottom = self._top - new_size[1]

        self._build_vertex_list()

# Only support pure horizontal or vertical lines, nothing angled
class Line(object):
    def __init__(self, batch, group, start, finish, thickness, color: Tuple[int, int, int, int]):
        self._color = color
        self._batch = batch
        self._thickness = thickness
        self.vertex_list = None
        self.group = group

        if start[0] != finish[0] and start[1] != finish[1]:
            raise Exception("Application does not support angled lines!")

        self._left, self._right = start[0], finish[0]
        self._top, self._bottom = start[1], finish[1]
        if self._left == self._right:
            self._left = start[0] - thickness // 2
            self._right = start[0] + thickness // 2
        else:
            self._top = start[1] - thickness // 2
            self._bottom = start[1] + thickness // 2

        self._build_vertex_list()

    def _build_vertex_list(self):
        if self.vertex_list:
            self.vertex_list.delete()

        if self._thickness == 1:
            self.vertex_list = self._batch.add(
                2, pyglet.gl.GL_LINES, self.group,
                ('v2i', [self._left, self._top, self._right, self._bottom]),
                ('c4B', self._color * 2)
            )
        else:
            self.vertex_list = self._batch.add(
                4, pyglet.gl.GL_QUADS, self.group,
                ('v2i', [self._left, self._top, self._right, self._top, self._right, self._bottom, self._left, self._bottom]),
                ('c4B', self._color * 4)
            )

    def delete(self):
        if self.vertex_list:
            self.vertex_list.delete()

    def get_color(self):
        return self._color

    def set_color(self, new_color):
        self._color = new_color
        self._build_vertex_list()
