# python version 3.5.0

import tkinter as tk
import tkinter.messagebox
from tile import *
from board import *
from PIL import Image
from PIL import ImageTk
from enum import Enum


class Minesweeper:

    def __init__(self, master):
        self.game_state = 0

        # set up frame
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.board = None

        self.start_new_game()
        

    def start_new_game(self):
        self.game_state = Game_State.PLAYING
        self.board = Board(5,12,15)

        # show "Minesweeper" at the top
        self.label1 = tk.Label(self.frame, text="Minesweeper")
        self.label1.grid(row = 0, column = 0, columnspan = self.board.width)

        for tile in self.board.tiles:
            tile.set_button(self.frame, self.board.image_unopened)
            tile.bind_button(self.left_click_event, self.right_click_event)
            tile.button.grid(row = tile.x + 1, column = tile.y)

        #add mine and count at the end
        self.label_num_mine = tk.Label(self.frame, text = "Mines: "+str(self.board.num_mines))
        self.label_num_mine.grid(row = self.board.height + 1, column = 0)

        self.label_num_flag = tk.Label(self.frame, text = "Flags: "+str(self.board.flags))
        self.label_num_flag.grid(row = self.board.height + 1, column = 4)

    def left_click_event(self, tile):
        if tile.mine and tile.state == Tile_State.BLANK: #if a mine
            # show all mines and check for flags
            for tile in self.board.tiles:
                if not tile.mine and tile.state == Tile_State.FLAG:
                    # change image to wrong image
                    pass
                if tile.mine and tile.state != Tile_State.FLAG:
                    tile.change_button_image(self.board.image_mine)
            # end game
            self.gameover()
        elif tile.state == Tile_State.BLANK:
            tile.state = Tile_State.CLICKED
            self.board.clicked += 1
            tile.unbind_left_button()
            #change image
            if not tile.nearby_mines and not tile.mine:
                tile.change_button_image(self.board.image_opened)
                self.board.reveal_ring(tile)
            elif not tile.mine:
                tile.change_button_image(self.board.image_num[tile.nearby_mines-1])
            # if not already set as clicked, change state and count
            if self.board.clicked == self.board.num_tiles - self.board.num_mines:
                self.victory()

    def right_click_event(self, tile):
        print("right clicked at", tile.x, tile.y)
        # if not clicked
        if tile.state == Tile_State.BLANK:
            tile.state = Tile_State.FLAG
            tile.change_button_image(self.board.image_flag)
            # if a mine
            if tile.mine:
                self.board.correct_flags += 1
            self.board.flags += 1
            self.board.increase_flags(tile)
            self.update_flags()
        # if flagged, unflag
        elif tile.state == Tile_State.FLAG:
            tile.state = Tile_State.QUESTION
            tile.change_button_image(self.board.image_question)
            #button_data[0].bind('<Button-1>', self.lclicked_wrapper(button_data[3]))
            # if a mine
            if tile.mine:
                self.board.correct_flags -= 1
            self.board.flags -= 1
            self.board.decrease_flags(tile)
            self.update_flags()
        elif tile.state == Tile_State.QUESTION:
            tile.state = Tile_State.BLANK
            tile.change_button_image(self.board.image_unopened)
        elif tile.state == Tile_State.CLICKED:
            if tile.nearby_flags == tile.nearby_mines:
                self.board.confirm_flags(tile, self.trigger_gameover)
                if self.game_state == Game_State.LOSS:
                    self.gameover()
                else:
                    self.board.reveal_ring(tile)
                    if self.board.clicked == self.board.num_tiles - self.board.num_mines:
                        self.victory()

    def update_flags(self):
        self.label_num_flag.config(text = "Flags: "+str(self.board.flags))

    def victory(self):
        print("you win")
        self.game_state = Game_State.WIN

    def trigger_gameover(self):
        self.game_state = Game_State.LOSS

    def gameover(self):
        print("you lose")
        self.game_state = Game_State.LOSS


class Game_State(Enum):
    NO_GAME = 0
    PLAYING = 1
    WIN = 2
    LOSS = 3


### END OF CLASSES ###

def config_menubar(master):
    menubar = tk.Menu(master)
    filemenu = tk.Menu(menubar, tearoff=0)
    # filemenu.add_command(label="New", command=donothing)
    # filemenu.add_command(label="Open", command=donothing)
    # filemenu.add_command(label="Save", command=donothing)
    # filemenu.add_separator()
    filemenu.add_command(label="Exit", command=master.quit, accelerator="Cmd+w")
    menubar.add_cascade(label="File", menu=filemenu)
     
    # helpmenu = tk.Menu(menubar, tearoff=0)
    # helpmenu.add_command(label="Help Index", command=donothing)
    # helpmenu.add_command(label="About...", command=donothing)
    # menubar.add_cascade(label="Help", menu=helpmenu)
     
    master.config(menu=menubar)

def donothing():
    pass

def main():
    global root
    # create Tk widget
    root = tk.Tk()
    # set program title
    root.title("Minesweeper")
    config_menubar(root)
    # create game instance
    minesweeper = Minesweeper(root)
    # run event loop
    root.mainloop()

if __name__ == "__main__":
    main()