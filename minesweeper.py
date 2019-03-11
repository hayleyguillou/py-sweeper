# python version 3.5.0

import tkinter as tk
import tkinter.messagebox
from PIL import Image
from PIL import ImageTk
import random

class Minesweeper:

    def __init__(self, master):
        self.height = 10
        self.width = 10
        self.num_tiles = self.width * self.height
        self.num_mines = 20

        # import images
        i_width = 20
        i_height = 20
        self.image_unopened = ImageTk.PhotoImage(Image.open("img/unopened.gif").resize((i_width,i_height), Image.ANTIALIAS))
        self.image_opened = ImageTk.PhotoImage(Image.open("img/opened.gif").resize((i_width,i_height), Image.ANTIALIAS))
        self.image_mine = ImageTk.PhotoImage(Image.open("img/mine.gif").resize((i_width,i_height), Image.ANTIALIAS))
        self.image_flag = ImageTk.PhotoImage(Image.open("img/flag.gif").resize((i_width,i_height), Image.ANTIALIAS))
        self.image_question = ImageTk.PhotoImage(Image.open("img/question.gif").resize((i_width,i_height), Image.ANTIALIAS))
        self.tile_no = [ImageTk.PhotoImage(Image.open("img/"+str(x)+".gif").resize((i_width,i_height), Image.ANTIALIAS)) for x in range(1,9)]
        # self.image_unopened = tk.PhotoImage(file = "img/unopened.gif")
        # self.image_opened = tk.PhotoImage(file = "img/opened.gif")
        # self.image_mine = tk.PhotoImage(file = "img/mine.gif")
        # self.image_flag = tk.PhotoImage(file = "img/flag.gif")
        # self.image_question = tk.PhotoImage(file = "img/question.gif")
        # self.tile_no = [tk.PhotoImage(file = "img/"+str(x)+".gif") for x in range(1,9)]

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
        self.buttons = dict({})
        x_coord = 0
        y_coord = 0
        for x in range(0, 100):
            mine = 1 if x in mines else 0
            # tile image changeable for debug reasons:
            img = self.image_unopened
            self.buttons[x] = Tile(x,frame, img, mine, x_coord, y_coord, self.height, self.width)
            self.buttons[x].bind_button(self.left_click_event, self.right_click_event)

            # calculate coords:
            y_coord += 1
            if y_coord == self.width:
                y_coord = 0
                x_coord += 1
        
        # lay buttons in grid
        for key in self.buttons:
            self.buttons[key].button.grid( row = self.buttons[key].x + 1, column = self.buttons[key].y )

        # find nearby mines and display number on tile


        #add mine and count at the end
        self.label_num_mine = tk.Label(frame, text = "Mines: "+str(self.num_mines))
        self.label_num_mine.grid(row = self.height + 1, column = 0, columnspan = self.width // 2)

        self.label_num_flag = tk.Label(frame, text = "Flags: "+str(self.flags))
        self.label_num_flag.grid(row = self.height + 1, column = self.width // 2 - 1, columnspan = self.width // 2)
        print("row = ",self.height + 1," column = ",self.width // 2 - 1," columnspan = ",self.width // 2)

    def left_click_event(self, event):
        print("left clicked at", event.x, event.y)

    def right_click_event(self, event):
        print("right clicked at", event.x, event.y)


class Tile:

    def __init__(self, tile_id, frame, img, mine, x, y, height, width):
        self.button = tk.Button(frame, image = img)
        self.mine = mine
        self.state = 0
        self.id = tile_id
        self.x = x
        self.y = y
        self.nearby_mines = 0
        self.onTop = x == 1
        self.onLeft = y == 0
        self.onRight = y == width - 1
        self.onBottom = x == height

    def bind_button(self, left_event, right_event):
        self.button.bind('<Button-1>', self.__click_wrapper(left_event))
        self.button.bind('<Button-2>', self.__click_wrapper(right_event)) # mac trackpads: 2 = right-click
        self.button.bind('<Button-3>', self.__click_wrapper(right_event))

    def __click_wrapper(self, func):
        return lambda Button: func(self)



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