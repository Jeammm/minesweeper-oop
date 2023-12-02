from tkinter import *
from tkmacosx import Button
from cell import Cell
import settings
import utils

root = Tk()

#settings
root.configure(bg="black")
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("Minesweeper Game")
root.resizable(False, False)

top_frame = Frame(
  root, 
  bg="grey",
  width=settings.WIDTH,
  height=utils.height_prct(10),
  )
top_frame.place(x=0, y=0)

center_frame = Frame(
  root,
  bg="green",
  width=utils.width_prct(90),
  height=utils.height_prct(80)
)
center_frame.place(
  x=utils.width_prct(5),
  y=utils.height_prct(15)
)

Cell.root = root

def start_game(event=None):
  
  Cell.all = []
  Cell.game_started = False
  Cell.game_ended = False
  Cell.time = 0
  Cell.cell_count = settings.CELL_COUNT - settings.MINES_COUNT
  
  if isinstance(Cell.cell_count_lable_object, Label):
    Cell.cell_count_lable_object.destroy()
    Cell.timer.destroy()
  
  for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
      c = Cell(x, y)
      c.create_btn_object(center_frame)
      c.cell_btn_object.grid(column=x, row=y)

  Cell.create_cell_count_label(top_frame)
  Cell.cell_count_lable_object.place(x=20, y=20)

  timer = Label(
    top_frame, 
    text=0,
    font=("",30),
    width=6
    )
  timer.place(x=settings.WIDTH-150, y=20)
  Cell.timer = timer
  
start_game()

restart_btn = Button(
  top_frame,
  text="Try again",
  borderless=1,
  takefocus=0,
  focuscolor='',
  fg="green",
  font=("", 23)
  )
restart_btn.bind('<Button-1>', start_game)
restart_btn.place(x=settings.WIDTH-350, y=20)

#Run the window
root.mainloop()