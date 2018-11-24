import pyglet
from swidget import UIElement

class Line(UIElement):
    def __init__(self, batch, start=(0, 0), finish=(50, 0), thickness=1, color=(0, 0, 0, 255), group=None, visible=True):
        if start[0] != finish[0] and start[1] != finish[1]:
            raise Exception("Application does not support angled lines!")

        if start[0] == finish[0]:
            width = thickness
            height = abs(start[1] - finish[1])
        else:
            width = abs(start[0] - finish[0])
            height = thickness

        UIElement.__init__(self, batch, group, start, (width, height), visible)

        self._start = start
        self._finish = finish

        # --- Properties ---
        self._color = color
        self._thickness = thickness
        self._true_color = color
        self.vertex_list = None

        self._render()

    def _render(self):
        if self.vertex_list:
            self.vertex_list.delete()

        self._true_color = self._color if self._visible else (0, 0, 0, 0)

        left, right = self._start[0], self._finish[0]
        top, bottom = (UIElement.SCREEN_HEIGHT - self._start[1]), (UIElement.SCREEN_HEIGHT - self._finish[1])
        if left == right:
            left = self._start[0] - self._thickness // 2
            right = self._start[0] + self._thickness // 2
        else:
            top = (UIElement.SCREEN_HEIGHT - self._start[1]) - self._thickness // 2
            bottom = (UIElement.SCREEN_HEIGHT - self._start[1]) + self._thickness // 2

        if self._thickness == 1:
            self.vertex_list = self.batch.add(
                2, pyglet.gl.GL_LINES, self.group,
                ('v2i', [left, top, right, bottom]),
                ('c4B', self._true_color * 2)
            )
        else:
            self.vertex_list = self.batch.add(
                4, pyglet.gl.GL_QUADS, self.group,
                ('v2i', [left, top, right, top, right, bottom, left, bottom]),
                ('c4B', self._true_color * 4)
            )

    def get_points(self):
        return self._start, self._finish

    def set_points(self, new_start=None, new_finish=None):
        self._start = new_start if new_start else self._start
        self._finish = new_finish if new_finish else self._finish

        if self._start[0] == self._finish[0]:
            width = self._thickness
            height = abs(self._start[1] - self._finish[1])
        else:
            width = abs(self._start[0] - self._finish[0])
            height = self._thickness

        # This call also renders the new changes
        self.set_size((width, height))

    def delete(self):
        if self.vertex_list:
            self.vertex_list.delete()

    def get_color(self):
        return self._color

    def set_color(self, new_color):
        self._color = new_color
        self._render()

    def get_thickness(self):
        return self._thickness

    def set_thickness(self, new_thickness):
        self._thickness = new_thickness
        if self._start[0] == self._finish[0]:
            width = self._thickness
            height = abs(self._start[1] - self._finish[1])
        else:
            width = abs(self._start[0] - self._finish[0])
            height = self._thickness

        # This call also renders the new changes
        self.set_size((width, height))