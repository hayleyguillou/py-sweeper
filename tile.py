import tkinter as tk
from enum import Enum

class Tile:

    def __init__(self, tile_id, mine, x, y, height, width, tile_size):
        self.button = None
        self.mine = mine
        self.state = Tile_State.BLANK
        self.tid = tile_id
        self.x = x
        self.y = y
        self.nearby_mines = 0
        self.nearby_flags = 0
        self.onTop = x == 0
        self.onLeft = y == 0
        self.onRight = y == width - 1
        self.onBottom = x == height - 1

    def set_button(self, frame, img):
        self.button = tk.Button(frame, image = img)

    def bind_button(self, left_event, right_event):
        self.button.bind('<Button-1>', self.__click_wrapper(left_event))
        self.button.bind('<Button-2>', self.__click_wrapper(right_event)) # mac trackpads: 2 = right-click
        self.button.bind('<Button-3>', self.__click_wrapper(right_event))

    def change_button_image(self, img):
        self.button.config(image = img)

    def __click_wrapper(self, func):
        return lambda Button: func(self)

    def unbind_left_button(self):
        self.button.unbind('<Button-1>')

class Tile_State(Enum):
    BLANK = 0
    FLAG = 1
    QUESTION = 2
    CLICKED = 3