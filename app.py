import pyglet
from window import MainWindow
from pyglet import window, text, gl, font
from pyglet.window import mouse



win = MainWindow()

# Allow transparency calculations
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

# Retrieve font from local folder
font.add_file('assets/fonts/Ubuntu-Medium.ttf')
font.load('Ubuntu Medium')

# Main application loop
pyglet.app.run()

