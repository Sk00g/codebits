import pyglet
from pyglet.window import mouse


# window = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
window = pyglet.window.Window(width=640, height=427)
window.set_caption('CODEBITS')

background = pyglet.resource.image('assets/pexels-photo-242236.jpeg')

pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
# window.push_handlers(pyglet.window.event.WindowEventLogger())

# text = pyglet.text.Label("CodeBits",
#                          font_name="Ubuntu Medium",
#                          font_size=22,
#                          color=(220, 220, 220, 255),
#                          x=window.width / 2, y=window.height / 2,
#                          anchor_x='center', anchor_y='center')

pyglet.font.add_file('assets/fonts/Ubuntu-Medium.ttf')
pyglet.font.load('Ubuntu Medium')

document = pyglet.text.decode_text('Hello World!')
document.set_style(0, 0, dict(font_name='Ubuntu Medium', font_size=22))
print(document.get_style('font_name'))
# document.text = 'Hello Scott!'
layout = pyglet.text.layout.TextLayout(document, 0, 0)
layout.x = 100
layout.y = 100
print(layout.content_width)
print(layout.content_height)


def timer_tick(dt):
    print('elapsed time: %s' % dt)

def one_shot(dt):
    print('once off: %s' % dt)

pyglet.clock.schedule_interval(timer_tick, 1.0)
pyglet.clock.schedule_once(one_shot, 2.0)


@window.event
def on_mouse_press(x, y, button, modifiers):
    print('mouse was pressed at %d, %d with button %s || (%s)' % (x, y, button, modifiers))


@window.event
def on_key_press(symbol, modifiers):
    print('key pressed %s || (%s)' % (symbol, modifiers))

    # Return True to prevent default window behaviour
    # return True


@window.event
def on_mouse_scroll(x, y, scrollx, scrolly):
    print('mouse scroll (%d, %d) + (%d, %d)' % (x, y, scrollx, scrolly))


@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2i', [0, 0, 640, 0, 640, 427, 0, 427]),
                         ('c4B', [20, 50, 50, 200] * 4))
    layout.draw()


pyglet.app.run()

# app will only exit when all windows are closed or pyglet.app.exit() is called