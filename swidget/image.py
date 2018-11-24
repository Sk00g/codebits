import pyglet
import os.path
from swidget import UIElement


class Image(UIElement):
    def __init__(self, batch, file_path, position=(0, 0), size=(-1, -1), group=None, visible=True):
        UIElement.__init__(self, batch, group, position, size, visible)

        self._image = pyglet.resource.image(file_path)
        self._sprite = pyglet.sprite.Sprite(self._image, batch=self.batch, group=group)

        self._scalex, self._scaley = (1, 1)
        self.set_size(size)

        self._render()

    def delete(self):
        self._sprite.delete()

    def set_size(self, new_size):
        self._size = new_size
        if new_size == (-1, -1):
            self._size = (self._sprite.width, self._sprite.height)

        self._scalex = self._size[0] / self._sprite.width
        self._scaley = self._size[1] / self._sprite.height

    def _render(self):
        self._sprite.visible = self._visible
        self._sprite.update(self._position[0], UIElement.SCREEN_HEIGHT - self._position[1] - self._size[1],
                            scale_x=self._scalex, scale_y=self._scaley)


