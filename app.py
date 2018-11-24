import pyglet
from window import MainWindow
from pyglet import gl, font


# Retrieve font from local folder
font.add_file('assets/fonts/Arimo-Regular.ttf')
font.load('Arimo')

# Globally accessible variable
win = MainWindow()

# Allow transparency calculations
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

# Debug all events
# win.push_handlers(pyglet.window.event.WindowEventLogger())

# Main application loop
pyglet.app.run()

