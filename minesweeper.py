# python version 3.5.0

import tkinter as tk
import tkinter.messagebox
from PIL import Image
from PIL import ImageTk
import random
from enum import Enum

class Minesweeper:

    def __init__(self, master):
        self.over = False

        self.height = 5
        self.width = 5
        self.num_tiles = self.width * self.height
        self.num_mines = 5

        # import images
        self.image_size = 20
        i = self.image_size
        # self.image_unopened = ImageTk.PhotoImage(Image.open("img/unopened.gif").resize((i,i), Image.ANTIALIAS))
        # self.image_opened = ImageTk.PhotoImage(Image.open("img/opened.gif").resize((i,i), Image.ANTIALIAS))
        # self.image_mine = ImageTk.PhotoImage(Image.open("img/mine.gif").resize((i,i), Image.ANTIALIAS))
        # self.image_flag = ImageTk.PhotoImage(Image.open("img/flag.gif").resize((i,i), Image.ANTIALIAS))
        # self.image_question = ImageTk.PhotoImage(Image.open("img/question.gif").resize((i,i), Image.ANTIALIAS))
        # self.image_num = [ImageTk.PhotoImage(Image.open("img/"+str(x)+".gif").resize((i,i), Image.ANTIALIAS)) for x in range(1,9)]
        self.image_unopened = tk.PhotoImage(file = "img/unopened.gif")
        self.image_opened = tk.PhotoImage(file = "img/opened.gif")
        self.image_mine = tk.PhotoImage(file = "img/mine.gif")
        self.image_flag = tk.PhotoImage(file = "img/flag.gif")
        self.image_question = tk.PhotoImage(file = "img/question.gif")
        self.image_num = [tk.PhotoImage(file = "img/"+str(x)+".gif") for x in range(1,9)]

        # set up frame
        frame = tk.Frame(master)
        frame.pack()

        # show "Minesweeper" at the top
        self.label1 = tk.Label(frame, text="Minesweeper")
        self.label1.grid(row = 0, column = 0, columnspan = self.width)

        # create flag and clicked tile variables
        self.flags = 0
        self.correct_flags = 0
        self.clicked = 0

        # generate mines
        mines = set()
        while len(mines) < self.num_mines:
            mines.add(random.randint(0,self.num_tiles-1))

        # create buttons
        self.tiles = []
        x_coord = 0
        y_coord = 0
        for tile_id in range(self.num_tiles):
            mine = 1 if tile_id in mines else 0
            # tile image changeable for debug reasons:
            img = self.image_unopened
            tile = Tile(tile_id, frame, img, mine, x_coord, y_coord, self.height, self.width, self.image_size)
            tile.bind_button(self.left_click_event, self.right_click_event)

            self.tiles.append(tile)

            # calculate coordinates:
            y_coord += 1
            if y_coord == self.width:
                y_coord = 0
                x_coord += 1
        
        for i,tile in enumerate(self.tiles):
            
            # lay buttons in grid
            tile.button.grid( row = tile.x + 1, column = tile.y, sticky="nsew")
            # get true tile image
            if not tile.mine:
                self.do_to_surrounding_tiles(tile, self.count_nearby_mines)
            print(tile.tid, tile.x, tile.y, tile.mine, tile.nearby_mines)

        #add mine and count at the end
        self.label_num_mine = tk.Label(frame, text = "Mines: "+str(self.num_mines))
        self.label_num_mine.grid(row = self.height + 1, column = 0, columnspan = 5)

        self.label_num_flag = tk.Label(frame, text = "Flags: "+str(self.flags))
        self.label_num_flag.grid(row = self.height + 1, column = 4, columnspan = 5)


    def count_nearby_mines(self, tile, index):
        if self.tiles[index].mine:
            tile.nearby_mines += 1


    def left_click_event(self, tile):
        if tile.mine and tile.state == Tile_State.BLANK: #if a mine
            # show all mines and check for flags
            for tile in self.tiles:
                if not tile.mine and tile.state == Tile_State.FLAG:
                    # change image to wrong image
                    pass
                if tile.mine and tile.state != Tile_State.FLAG:
                    tile.button.config(image = self.image_mine)
            # end game
            self.gameover()
        else:
            self.reveal_tile(tile)

    def right_click_event(self, tile):
        print("right clicked at", tile.x, tile.y)
        # if not clicked
        if tile.state == Tile_State.BLANK:
            tile.state = Tile_State.FLAG
            tile.button.config(image = self.image_flag)
            #button_data[0].unbind('<Button-1>')
            # if a mine
            if tile.mine:
                self.correct_flags += 1
            self.flags += 1
            self.do_to_surrounding_tiles(tile, self.increase_nearby_flags)
            self.update_flags()
        # if flagged, unflag
        elif tile.state == Tile_State.FLAG:
            tile.state = Tile_State.QUESTION
            tile.button.config(image = self.image_question)
            #button_data[0].bind('<Button-1>', self.lclicked_wrapper(button_data[3]))
            # if a mine
            if tile.mine:
                self.correct_flags -= 1
            self.flags -= 1
            self.do_to_surrounding_tiles(tile, self.decrease_nearby_flags)
            self.update_flags()
        elif tile.state == Tile_State.QUESTION:
            tile.state = Tile_State.BLANK
            tile.button.config(image = self.image_unopened)
        elif tile.state == Tile_State.CLICKED:
            if tile.nearby_flags == tile.nearby_mines:
                self.do_to_surrounding_tiles(tile, self.check_correct_flag)
                if not self.over:
                    self.do_to_surrounding_tiles(tile, self.show_empty_tiles)


    def increase_nearby_flags(self, tile, index):
        self.tiles[index].nearby_flags += 1

    def decrease_nearby_flags(self, tile, index):
        self.tiles[index].nearby_flags -= 1

    def check_correct_flag(self, tile, index):
        if self.tiles[index].state == Tile_State.FLAG and not self.tiles[index].mine:
            self.gameover()

    def reveal_tile(self, tile):
        if tile.state != Tile_State.CLICKED:
            tile.state = Tile_State.CLICKED
            self.clicked += 1
            #change image
            if not tile.nearby_mines and not tile.mine:
                tile.button.config(image = self.image_opened)
                self.do_to_surrounding_tiles(tile, self.show_empty_tiles)
            elif not tile.mine:
                tile.button.config(image = self.image_num[tile.nearby_mines-1])
            # if not already set as clicked, change state and count
            if self.clicked == self.num_tiles - self.num_mines:
                self.victory()


    def show_empty_tiles(self, tile, index):
        self.reveal_tile(self.tiles[index])

    def show_tiles(self, tile, index):
        self.show_empty_tiles(tile, index)

    def do_to_surrounding_tiles(self, tile, function):
        # above
        if not tile.onTop:
            index = tile.tid - self.width
            function(tile, index)
            # above left
            if not tile.onLeft:
                index = tile.tid - self.width - 1
                function(tile, index)
            # above right
            if not tile.onRight:
                index = tile.tid - self.width + 1
                function(tile, index)
        # below
        if not tile.onBottom:
            index = tile.tid + self.width
            function(tile, index)
            # below left
            if not tile.onLeft:
                index = tile.tid + self.width - 1
                function(tile, index)
            # below right
            if not tile.onRight:
                index = tile.tid + self.width + 1
                function(tile, index)
        # left
        if not tile.onLeft:
            index = tile.tid - 1
            function(tile, index)
        # right
        if not tile.onRight:
            index = tile.tid + 1
            function(tile, index)




    def update_flags(self):
        self.label_num_flag.config(text = "Flags: "+str(self.flags))

    def victory(self):
        print("you win")

    def gameover(self):
        print("you lose")



class Tile:

    def __init__(self, tile_id, frame, img, mine, x, y, height, width, tile_size):
        self.button = tk.Button(frame, image = img)
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

    def bind_button(self, left_event, right_event):
        self.button.bind('<Button-1>', self.__click_wrapper(left_event))
        self.button.bind('<Button-2>', self.__click_wrapper(right_event)) # mac trackpads: 2 = right-click
        self.button.bind('<Button-3>', self.__click_wrapper(right_event))

    def __click_wrapper(self, func):
        return lambda Button: func(self)

class Tile_State(Enum):
    BLANK = 0
    FLAG = 1
    QUESTION = 2
    CLICKED = 3



### END OF CLASSES ###

def main():
    global root
    # create Tk widget
    root = tk.Tk()
    # set program title
    root.title("Minesweeper")
    # create game instance
    minesweeper = Minesweeper(root)
    # run event loop
    root.mainloop()

if __name__ == "__main__":
    main()