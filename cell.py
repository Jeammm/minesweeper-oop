from tkmacosx import Button
from tkinter import Label
import random
import settings
import utils

class Cell:
  all = []
  cell_count_lable_object = None
  cell_count = settings.CELL_COUNT - settings.MINES_COUNT
  game_started = False
  game_ended = False
  root = None
  time = 0
  timer = None
  
  def ticking():
    Cell.time += 1
    Cell.timer.configure(text=Cell.time)
    
    if not Cell.game_ended:
      Cell.root.after(1000, Cell.ticking)

  
  def __init__(self, x, y, is_mine=False):
    self.is_mine = is_mine
    self.cell_btn_object = None
    self.x = x
    self.y = y
    
    self.is_opened = False
    self.is_flagged = False
    
    Cell.all.append(self)
    
  def create_btn_object(self, location):
    btn_size = utils.width_prct(90) // settings.GRID_SIZE
    
    btn = Button(
      location,
      width=btn_size,
      height=btn_size,
      borderless=1,
      takefocus=0,
      focuscolor='',
      fg="SystemButtonFace",
      font=("", 23)
    )
    btn.bind('<Button-1>', self.left_click_actions)
    btn.bind('<Button-2>', self.right_click_actions)
    self.cell_btn_object = btn
    
  def left_click_actions(self, event):
    #spread the mines after selecing first cell
    if Cell.game_ended:
      return
    
    if not Cell.game_started:
      Cell.randomized_mines(self.x, self.y)
      Cell.game_started = True
      Cell.root.after(1000, Cell.ticking)
    
    if self.is_flagged:
      return
    
    if self.is_opened:
      self.area_cleared()
      return
    
    self.show_cell()
  
  def explode(self):
    self.is_opened = True
    Cell.game_ended = True
    for cell in Cell.all:
      if cell.is_mine:
        cell.cell_btn_object.configure(bg="red")
    self.cell_btn_object.configure(
      bg="#630000"
      )
  def get_cells_by_axis(self, x, y):
    for cell in Cell.all:
      if cell.x == x and cell.y == y:
        return cell
  
  @property
  def surrounded_cells(self):
    cells = []
    for x_offset in [-1, 0, 1]:
      for y_offset in [-1, 0, 1]:
        target_x = self.x + x_offset
        target_y = self.y + y_offset
        if target_x < 0 or target_x >= settings.GRID_SIZE:
          continue
        if target_y < 0 or target_y >= settings.GRID_SIZE:
          continue
        
        cell = self.get_cells_by_axis(target_x, target_y)
        cells.append(cell)
    return cells
  
  @property
  def count_surrounded_mines(self):
    mines_count = 0
    
    for cell in self.surrounded_cells:
      if cell.is_mine:
        mines_count += 1
    return mines_count
    
  
  def show_cell(self):
    if self.is_mine:
      self.explode()
      return
    
    if not self.is_opened:
      Cell.cell_count -= 1
      Cell.cell_count_lable_object.configure(text=f"Cells Left: {Cell.cell_count}")
    
    mines_count_to_show = self.count_surrounded_mines
    if mines_count_to_show == 0:
      mines_count_to_show = ""
      
    self.cell_btn_object.configure(text=mines_count_to_show, bg="grey")
    self.is_opened = True
    
    if self.count_surrounded_mines == 0:
      for cell in self.surrounded_cells:
        if not cell.is_opened:
          cell.show_cell()
    if Cell.cell_count == 0:
      Cell.game_ended = True
      for cell in Cell.all:
        if not cell.is_mine:
          cell.cell_btn_object.configure(bg="green")
    
  def area_cleared(self):
    flagged_count = 0
    for cell in self.surrounded_cells:
      if cell.is_flagged:
        flagged_count += 1
    if flagged_count == self.count_surrounded_mines:
      for cell in self.surrounded_cells:
        if not cell.is_flagged:
          cell.show_cell()
    
  def right_click_actions(self, event):
    if Cell.game_ended:
      return
    
    if self.is_opened:
      return
    
    if not self.is_flagged:
      self.cell_btn_object.configure(bg="orange")
      self.is_flagged = True
    else:
      self.cell_btn_object.configure(bg="white")
      self.is_flagged = False
  
  @staticmethod
  def randomized_mines(x, y):
    filtered_cells = [cell for cell in Cell.all if cell.x != x and cell.y != y]
    picked_cells = random.sample(filtered_cells, settings.MINES_COUNT)
    for cell in picked_cells:
      cell.is_mine = True
      
  @staticmethod
  def create_cell_count_label(location):
    lbl = Label(
      location,
      text=f"Cells Left: {Cell.cell_count}",
      font=("",30)
    )
    Cell.cell_count_lable_object = lbl
  
  def __repr__(self):
    return f"Cell({self.x},{self.y})"
  
  