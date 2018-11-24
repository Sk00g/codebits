import pyglet
from swidget import UIElement

class Rectangle(UIElement):
    def __init__(self, batch, position=(0, 0), size=(50, 50), color=(0, 0, 0, 255), group=None, visible=True):
        UIElement.__init__(self, batch, group, position, size, visible)

        # --- Properties ---
        self._color = color
        self._true_color = color
        self._left, self._right, self._top, self._bottom = [None] * 4
        self.vertex_list = None

        self._render()

    def _render(self):
        self._left = self._position[0]
        self._right = self._position[0] + self._size[0]
        self._top = UIElement.SCREEN_HEIGHT - self._position[1]
        self._bottom = self._top - self._size[1]

        self._true_color = self._color if self._visible else (0, 0, 0, 0)

        if self.vertex_list:
            self.vertex_list.delete()

        self.vertex_list = self.batch.add(
            4, pyglet.gl.GL_QUADS, self.group,
            ('v2i',
             [self._left, self._top, self._right, self._top, self._right, self._bottom, self._left, self._bottom]),
            ('c4B', self._true_color * 4)
        )

    def delete(self):
        if self.vertex_list:
            self.vertex_list.delete()

    def get_color(self):
        return self._color

    def set_color(self, new_color):
        self._color = new_color
        self._render()