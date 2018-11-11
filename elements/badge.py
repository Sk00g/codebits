import pyglet
from enums import *



class Badge(object):
    def __init__(self, batch, location, text, border, background):
        self.batch = batch
        self.location = location

        self.border_color = {
            ControlState.DEFAULT: border,
            ControlState.HOVER: (min(border[0] + 30, 255), min(border[1] + 30, 255), min(border[2] + 30, 255), 255)
        }

        self.background_color = {
            ControlState.DEFAULT: background,
            ControlState.HOVER: background
        }

