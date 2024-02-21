import tkinter as tk
from tkinter.simpledialog import askstring, askinteger
from  tkinter.filedialog import askopenfile
from random import randrange as rr
import json


class Box(tk.Button):
    def __init__(self, master, x: int, y: int, is_pressed: bool = False) -> None:
        super(Box, self).__init__(master, width=3, font='Calibri 10 bold')
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
    ROWS = 30
    COLUMNS = 45

    buttons = []

    window = tk.Tk()
    # window.resizable(False, False)

    def __init__(self, skip: bool = False) -> None:
        self.window.bind_all('<KeyPress-Up>', self.step)

        if skip:
            return

        for i in range(self.ROWS):
            f = []
            for j in range(self.COLUMNS):
                box = Box(self.window, i, j)
                box.config(command=lambda btn=box: self.click(btn))
                f.append(box)
            self.buttons.append(f)

    def clear(self) -> None:
        self.destroy()

        btns = []

        for i in range(self.ROWS):
            f = []
            for j in range(self.COLUMNS):
                box = Box(self.window, i, j)
                box.config(command=lambda btn=box: self.click(btn))
                f.append(box)
            btns.append(f)
        
        self.saving(btns)
    
    def save(self) -> None:
        filename = askstring('tk', 'Введите название файла.')

        state = []
        for row in self.buttons:
            state_row = []
            for btn in row:
                state_row.append(int(btn.is_pressed))
            state.append(state_row)

        state_end = [[self.ROWS, self.COLUMNS], state]

        with open(f'{filename}.ca', 'wt') as f:
            json.dump(state_end, f, indent=2)
    
    def load(self) -> None:
        with askopenfile('tr') as f:
            full_object = json.load(f)
        
        self.ROWS = full_object[0][0]
        self.COLUMNS = full_object[0][1]
    
        self.destroy()
        
        buttons = []
        for y in range(len(full_object[1])):
            row = []
            for x in range(len(full_object[1][y])):
                btn = Box(self.window, y, x, is_pressed=bool(full_object[1][y][x]))
                btn.config(command=lambda b=btn: self.click(b))
                if full_object[1][y][x]:
                    btn.pressed()
                else:
                    btn.not_pressed()
                row.append(btn)
            buttons.append(row)
        
        self.saving(buttons)

    def destroy(self) -> None:
        [child.destroy() for child in self.window.winfo_children()]

    def saving(self, btns) -> None:
        self.buttons = btns
        self.__init__(skip=True)
        self.start()

    def create_widgets(self):
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        file = tk.Menu(menu_bar, tearoff=0)

        file.add_command(label='Сохранить', command=self.save)
        file.add_command(label='Загрузить', command=self.load)
        file.add_command(label='Настройки', command=self.settings)
        menu_bar.add_cascade(label='Файл', menu=file)

        do = tk.Menu(menu_bar, tearoff=0)

        do.add_command(label='Случайное заполнение', command=self.random_fill)
        do.add_command(label='Очистить', command=self.clear)
        menu_bar.add_cascade(label='Действия', menu=do)

    def random_fill(self):
        full_prc = askinteger('tk', 'Введите процент заполнения поля.')

        self.destroy()

        buttons = []

        for y in range(self.ROWS):
            temp = []
            for x in range(self.COLUMNS):
                btn = Box(self.window, y, x)
                btn.config(command=lambda x=btn: self.click(btn))
                num = rr(1,101)
                if num <= full_prc:
                    btn.pressed()
                else:
                    btn.not_pressed()
                temp.append(btn)
            buttons.append(temp)

        self.saving(buttons)

    def settings(self) -> None:
        crows = askinteger('tk', 'Введите количество строк.')
        ccolumns = askinteger('tk', 'Введите количество колонок.')

        self.ROWS = crows
        self.COLUMNS = ccolumns

        self.clear()

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
                box.grid(row=box.x, column=box.y, stick='NSEW')

    def start(self) -> None:
        self.grid()
        self.create_widgets()
        self.window.mainloop()


if __name__ == '__main__':
    app = App()
    app.start()
