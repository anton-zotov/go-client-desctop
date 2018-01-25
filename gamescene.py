import time
from tkinter import *
from PIL import Image, ImageTk
from scene import Scene
from cell import Cell
from threading import Thread


class GameScene(Scene):
    def __init__(self, client):
        super(GameScene, self).__init__(client.master)
        self.client = client
        self.canvas = Canvas(self.frame, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)
        self.my_turn = False
        self.is_game_over = False
        self.polling = False
        self.load_images()
        self.__create_interface()

        self.init_game()
        self.canvas.bind("<Button-1>", self.on_LMB_click)
        self.canvas.bind("<Configure>", self.__configure)

    def __create_interface(self):
        font = "Helvetica 20"
        self.turn_label = Label(self.frame, text="", font=font)
        self.pass_button = Button(self.frame, text="Pass", command=self.skip_turn)

    def __configure(self, event):
        self.__redraw_canvas(event)
        self.__configure_interface()

    def __configure_interface(self):
        width = self.frame.winfo_width()
        height = self.frame.winfo_height()
        self.turn_label.place(x=width / 2 - 150, y=10, width=300, height=36)
        self.pass_button.place(x=width / 2 - 150, y=height - 46, width=300, height=36)

    def __redraw_canvas(self, event):
        self.canvas.delete("all")
        self.canvas.config(width=event.width, height=event.height)
        self.canvas.create_rectangle(0, 0, event.width, event.height, fill="#FCB040")
        self.calc_cell_size()
        self.resize_images()
        self.grid(False)

    def __set_turn(self, my_turn):
        self.my_turn = my_turn
        if self.is_game_over:
            self.turn_label.config("Gave is over")
        else:
            self.turn_label.config(text="Your turn" if my_turn else "Waiting for opponent")
        self.pass_button.config(state="normal" if my_turn and not self.is_game_over else "disabled")

    def load_images(self):
        self.orig_images = {}
        self.orig_images["white_stone"] = Image.open("images/white_stone.png")
        self.orig_images["black_stone"] = Image.open("images/black_stone.png")

    def resize_images(self):
        self.images = {}
        stone_size = int(self.cell_size * 0.8)
        self.images["white_stone"] = ImageTk.PhotoImage(self.orig_images["white_stone"].resize((stone_size, stone_size)))
        self.images["black_stone"] = ImageTk.PhotoImage(self.orig_images["black_stone"].resize((stone_size, stone_size)))

    def calc_cell_size(self):
        self.cell_size = min(int(self.canvas['width']), int(self.canvas['height'])) / (self.field_size + 2)

    def grid(self, create_grid=True):
        if create_grid:
            self.cells = []
        x_offset = 0
        y_offset = 0
        width = int(self.canvas['width'])
        height = int(self.canvas['height'])
        if width > height:
            x_offset = (width - height) / 2
        else:
            y_offset = (height - width) / 2

        x_offset += self.cell_size
        y_offset += self.cell_size

        for i in range(self.field_size):
            for j in range(self.field_size):
                x = self.cell_size * i + x_offset
                y = self.cell_size * j + y_offset
                if create_grid:
                    self.cells.append(Cell(self, i, j, x, y, self.cell_size))
                else:
                    self.cells[i * self.field_size + j].config(x, y, self.cell_size)
                    self.cells[i * self.field_size + j].draw()

    def on_LMB_click(self, event):
        for cell in self.cells:
            if cell.check_click(event.x, event.y):
                self.on_cell_click(cell)

    def on_cell_click(self, cell):
        print(cell.col, cell.row)
        if (self.try_put_stone(cell)):
            pass

    def try_put_stone(self, cell):
        if not self.my_turn or cell.stone:
            return False
        if self.client.put_stone(cell.col, cell.row):
            cell.put_stone(self.color)
            self.__set_turn(False)

    def init_game(self):
        game_data = self.client.get_game_data()
        if game_data:
            print(game_data)
            self.field_size = game_data['field_size']
            self.color = game_data['color']
            self.calc_cell_size()
            self.grid()
            self.__set_turn(game_data['your_turn'])
            self.resize_images()
            self.fill_field(game_data['field'])
            self.start_polling_thread()

    def fill_field(self, field):
        for cell in self.cells:
            index = cell.row * self.field_size + cell.col
            if field[index] == 'w':
                cell.put_stone('white')
            if field[index] == 'b':
                cell.put_stone('black')

    def start_polling_thread(self):
        self.polling = True
        thread = Thread(target=self.polling_thread)
        thread.daemon = True
        thread.start()

    def polling_thread(self):
        while self.polling:
            print("get_game_update")
            self.client.get_game_update(self.process_events, self)
            time.sleep(0.5)

    def process_events(self, events):
        print("events", events)
        for event in events:
            if event['type'] == 'put':
                x, y, color = event['data']
                cell = self.get_cell(x, y)
                cell.put_stone(color)
            if event['type'] == 'your_turn':
                self.__set_turn(True)
            if event['type'] == 'die':
                x, y = event['data']
                cell = self.get_cell(x, y)
                print("stone", x, y, cell.stone)
                cell.die()
            if event['type'] == 'game_over':
                self.game_over()

    def get_cell(self, col, row):
        for cell in self.cells:
            if cell.row == int(row) and cell.col == int(col):
                return cell

    def skip_turn(self):
        self.client.skip_turn()
        self.__set_turn(False)

    def game_over(self):
        self.is_game_over = True
        self.__set_turn(False)
