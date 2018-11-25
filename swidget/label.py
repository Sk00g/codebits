import pyglet
from swidget import UIElement
from swidget.theme import Basic


class Label(UIElement):
    def __init__(self, batch, position=(0, 0), text="label", font_name="Arimo", font_color=Basic.OFFWHITE,
                 font_size=12, group=None, visible=True):

        self._document = pyglet.text.document.FormattedDocument(text)
        self.set_style(0, len(text), dict(font_name=font_name, color=font_color, font_size=font_size))

        self._layout = pyglet.text.layout.IncrementalTextLayout(self._document, 0, 0, wrap_lines=False, group=group,
                                                                multiline=False, batch=batch)
        self._layout.width = self._layout.content_width
        self._layout.height = self._layout.content_height

        size = (self._layout.content_width, self._layout.content_height)
        UIElement.__init__(self, batch, group, position, size, visible)


        self._render()

    def delete(self):
        self._layout.delete()

    def _render(self):
        if not self._visible:
            self._layout.batch = None
        else:
            self._layout.batch = self.batch

        self._layout.x, self._layout.y = (self._position[0], UIElement.SCREEN_HEIGHT - self._position[1] - self._size[1])

    def get_text(self):
        return self._document.text

    def set_text(self, new_text):
        self._document.text = new_text
        self._layout.width = self._layout.content_width
        self._layout.height = self._layout.content_height
        self._size = self._layout.width, self._layout.height
        self._render()

    def set_style(self, start, end, new_style: dict):
        self._document.set_style(start, end, new_style)

    def get_style(self, key, start, end):
        return self._document.get_style_range(key, start, end)


