import pyglet


# window = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
window = pyglet.window.Window(width=640, height=427)
window.set_caption('CODEBITS')

background = pyglet.resource.image('assets/pexels-photo-242236.jpeg')

pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

text = pyglet.text.Label("CodeBits",
                         font_name="Ubuntu Medium",
                         font_size=24,
                         color=(220, 220, 220, 255),
                         x=window.width / 2, y=window.height / 2,
                         anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2i', [0, 0, 640, 0, 640, 427, 0, 427]),
                         ('c4B', [20, 50, 50, 200] * 4))
    text.draw()


pyglet.app.run()