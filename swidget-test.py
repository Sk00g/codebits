import pyglet
from pyglet import window, gl
from pyglet.window import key
from swidget import UIElement, Rectangle, Line, Label, Image



win = window.Window(width=640, height=480, caption="Test Window")
batch = pyglet.graphics.Batch()
UIElement.SCREEN_HEIGHT = win.height

# Allow transparency calculations
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

group_bkgr = pyglet.graphics.OrderedGroup(0)
group_front = pyglet.graphics.OrderedGroup(1)

back = Rectangle(batch, group=group_front, position=(50, 50), size=(20, 20), color=(255, 0, 0, 255))
front = Rectangle(batch, group=group_bkgr, position=(60, 60), size=(20, 20), color=(0, 255, 0, 255))

line1 = Line(batch, group=group_front, start=(300, 100), finish=(500, 100), color=(255, 0, 0, 255))
line2 = Line(batch, group=group_front, start=(320, 100), finish=(320, 240), color=(0, 255, 0, 255))

title = Label(batch, group=group_front, position=(50, 50), text="Hello Scott")

icon = Image(batch, 'assets/search2-purple.png', (200, 200), group=group_front)


def main():
    pyglet.app.run()

@win.event
def on_draw():
    win.clear()
    batch.draw()

@win.event
def on_key_press(symbol, modifiers):
    if symbol == key.V:
        icon.center(x=UIElement.SCREEN_WIDTH // 2, y=100)
    elif symbol == key.S:
        icon.set_visible(False)
    elif symbol == key.D:
        icon.set_visible(True)
    elif symbol == key.F:
        icon.set_position((10, 10))



# Entry point
main()


