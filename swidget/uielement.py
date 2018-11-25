import pyglet


class UIElement(object):
    # Set this during initialization
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480

    def __init__(self, batch, group=None, position=(0, 0), size=(0, 0), visible=True):
        if not batch:
            raise Exception("All swidget UIElements must have an associated batch object")

        # --- PUBLIC ---
        self.batch = batch
        self.group = group

        # --- PROPERTIES ---
        self._visible = visible
        self._position = position
        self._size = size

    def set_visible(self, flag):
        self._visible = flag
        self._render()

    def get_visible(self):
        return self._visible

    def set_position(self, new_position):
        self._position = new_position
        self._render()

    def get_position(self):
        return self._position

    def center(self, x=-1, y=-1):
        newx, newy = self._position

        if x != -1:
            newx = x - (self._size[0] // 2)
        if y != -1:
            newy = y - (self._size[1] // 2)
        self.set_position((newx, newy))

    def set_size(self, new_size):
        self._size = new_size
        self._render()

    def get_size(self):
        return self._size

    def is_point_within(self, point):
        return (0 < point[0] - self._position[0] < self._size[0] and
                0 < (UIElement.SCREEN_HEIGHT - point[1]) - self._position[1] < self._size[1])

    def __repr__(self):
        return 'UIElement (%d, %d)' % self._position


    # --- Abstract Methods ---

    """
    Run when any 'visual' properties are changed, re-creates vertexs, re-position text, re-position images, etc. 
    """
    def _render(self):
        raise NotImplementedError()

    """
    Remove this element from its batch and from memory. Use 'set_visible()' for a temporary removal 
    """
    def delete(self):
        raise NotImplementedError()


