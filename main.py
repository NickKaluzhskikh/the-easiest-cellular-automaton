import tkinter as tk


class Box(tk.Button):
    def __init__(self, master, x: int, y: int) -> None:
        super(Box, self).__init__(master, width=3, )
        self.x = x
        self.y = y
        self.is_pressed = False
        self.will_do = False

    def not_pressed(self) -> None:
        self.is_pressed = False
        self.config(bg='#F0F0F0')
        self.will_do = False

    def pressed(self) -> None:
        self.is_pressed = True
        self.config(bg='black')
        self.will_do = False


class App:
    ROWS = 20
    COLUMNS = 20

    buttons = []

    window = tk.Tk()

    def __init__(self) -> None:
        self.window.bind_all('<KeyPress-Up>', self.step)

        for i in range(self.ROWS):
            f = []
            for j in range(self.COLUMNS):
                box = Box(self.window, i, j)
                box.config(command=lambda btn=box: self.click(btn))
                f.append(box)
            self.buttons.append(f)

    def step(self, _) -> None:
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                box = self.buttons[i][j]
                scores = self.scores(box)
                if box.is_pressed:
                    if scores != 2 and scores != 3:
                        box.will_do = True
                else:
                    if scores == 3:
                        box.will_do = True
        for g in range(self.ROWS):
            for h in range(self.COLUMNS):
                box = self.buttons[g][h]
                if not box.will_do:
                    continue

                if box.is_pressed:
                    box.not_pressed()
                else:
                    box.pressed()

    def click(self, box: Box) -> None:
        if box.is_pressed:
            box.not_pressed()
        else:
            box.pressed()
        print('', end='')

    def scores(self, box: Box) -> int:
        count = 0
        for f in [-1, 0, 1]:
            for g in [-1, 0, 1]:

                if f == 0 and g == 0:
                    continue
                
                try:
                    box2 = self.buttons[box.x + f][box.y + g]
                except IndexError:
                    continue
                if box2.is_pressed:
                    count += 1
        return count

    def grid(self) -> None:
        for i in self.buttons:
            for box in i:
                box.grid(row=box.x, column=box.y)

    def start(self) -> None:
        self.grid()
        self.window.mainloop()


if __name__ == '__main__':
    app = App()
    app.start()
