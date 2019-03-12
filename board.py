import tkinter as tk
import random
from tile import *


class Board:
    def __init__(self, height, width, num_mines):
        self.height = height
        self.width = width
        self.num_tiles = width * height
        self.num_mines = num_mines

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

        # create flag and clicked tile variables
        self.flags = 0
        self.correct_flags = 0
        self.clicked = 0

        # generate mines
        self.mines = set()
        while len(self.mines) < self.num_mines:
            self.mines.add(random.randint(0,self.num_tiles-1))

        # create buttons
        self.tiles = []
        x_coord = 0
        y_coord = 0
        for tile_id in range(self.num_tiles):
            mine = 1 if tile_id in self.mines else 0
            # tile image changeable for debug reasons:
            img = self.image_unopened
            tile = Tile(tile_id, mine, x_coord, y_coord, self.height, self.width, self.image_size)

            self.tiles.append(tile)

            # calculate coordinates:
            y_coord += 1
            if y_coord == self.width:
                y_coord = 0
                x_coord += 1
        
        for i,tile in enumerate(self.tiles):
            # get true tile image
            if not tile.mine:
                self.__do_to_surrounding_tiles(tile, self.count_nearby_mines)


    def count_nearby_mines(self, tile, index):
        if self.tiles[index].mine:
            tile.nearby_mines += 1

    def increase_flags(self, tile):
        def increase_nearby_flags(tile, index):
            self.tiles[index].nearby_flags += 1
        self.__do_to_surrounding_tiles(tile, increase_nearby_flags)

    def decrease_flags(self, tile):
        def decrease_nearby_flags(tile, index):
            self.tiles[index].nearby_flags -= 1
        self.__do_to_surrounding_tiles(tile, decrease_nearby_flags)

    def confirm_flags(self, tile, gameover):
        def check_correct_flag(tile, index):
            if self.tiles[index].state == Tile_State.FLAG and not self.tiles[index].mine:
                gameover()
        self.__do_to_surrounding_tiles(tile, check_correct_flag)

    def reveal_ring(self, tile):
        self.__do_to_surrounding_tiles(tile, self.__reveal_tile_helper)

    def reveal_mines(self):
        for tile in self.tiles:
            tile.unbind_button()
            if not tile.mine and tile.state == Tile_State.FLAG:
                # change image to wrong image
                tile.button.config(bg="red")
                pass
            if tile.mine and tile.state != Tile_State.FLAG:
                tile.change_button_image(self.image_mine)
    

    def reveal_tile(self, tile):
        if tile.state != Tile_State.CLICKED and not tile.mine:
            tile.state = Tile_State.CLICKED
            self.clicked += 1
            tile.unbind_left_button()
            #change image
            if not tile.nearby_mines and not tile.mine:
                tile.button.config(image = self.image_opened)
                self.__do_to_surrounding_tiles(tile, self.__reveal_tile_helper)
            elif not tile.mine:
                tile.button.config(image = self.image_num[tile.nearby_mines-1])

    def __reveal_tile_helper(self, tile, index):
        self.reveal_tile(self.tiles[index])

    def __do_to_surrounding_tiles(self, tile, function):
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

    