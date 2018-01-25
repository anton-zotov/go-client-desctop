class Cell():
    def __init__(self, parent, col, row, x, y, size):
        self.parent = parent
        self.col = col
        self.row = row
        self.stone = None
        self.image = None
        self.config(x, y, size)

    def __draw_stone(self):
        if self.stone:
            self.image = self.parent.canvas.create_image(self.x + self.size / 2, self.y + self.size / 2,
                                                         image=self.parent.images[self.stone + "_stone"])

    def __erase(self):
        if self.image:
            self.parent.canvas.delete(self.image)
            self.image = None

    def config(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self):
        if self.col < self.parent.field_size - 1:
            self.parent.canvas.create_line(self.x + self.size / 2, self.y + self.size / 2, self.x + self.size + 1, self.y + self.size / 2)
        if self.col > 0:
            self.parent.canvas.create_line(self.x + self.size / 2, self.y + self.size / 2, self.x, self.y + self.size / 2)
        if self.row < self.parent.field_size - 1:
            self.parent.canvas.create_line(self.x + self.size / 2, self.y + self.size / 2, self.x + self.size / 2, self.y + self.size + 1)
        if self.row > 0:
            self.parent.canvas.create_line(self.x + self.size / 2, self.y + self.size / 2, self.x + self.size / 2, self.y)
        self.parent.canvas.create_text(self.x+self.size / 2, self.y+self.size / 2, text=str(self.col)+','+str(self.row))
        self.__draw_stone()

    def check_click(self, x, y):
        if (x >= self.x and x <= self.x + self.size and
                y >= self.y and y <= self.y + self.size):
            return True
        return False

    def put_stone(self, color):
        self.stone = color
        self.__erase()
        self.__draw_stone()

    def die(self):
        print("die bitch", self.col, self.row, self.stone)
        self.stone = None
        self.__erase()
