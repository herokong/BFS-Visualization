import pygame
import math
from queue import PriorityQueue, Queue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("GRAPH")

WHITE = (255, 255, 255)
GREY = (128,128,128)
BLACK = (0, 0, 0)
GREEN = (50,205,50)
BLUE = (0, 128, 128)
RED = (255,0,0)

# Stack datastructure for path construction.
class LinkedStackOfStrings():
    def __init__(self):
        self.first = self.Node()

    class Node():
        def __init__(self,string=None,node=None):
                self.item = string
                self.next = node
    
    def is_empty(self):
        return (self.first.next == None)

    def push(self,item):
        old_first = self.first
        self.first = self.Node()
        self.first.item = item
        self.first.next = old_first
    
    def pop(self):
        item = self.first.item
        self.first = self.first.next
        return item

# Helping function
def get_key(dic, val):
  """
  Return key of item in python dictionary.
  """
  for key in dic:
    if dic[key] == val:
      return key

# Spot class
class Node:
  def __init__(self, row, col, width, total_rows):
    self.row = row
    self.col = col
    self.x = row * width
    self.y = col * width
    self.color = WHITE
    self.neighbors = []
    self.width = width
    self.total_rows = total_rows

  def get_pos(self):
    return self.row, self.col
  
  def is_barrier(self):
    return self.color == BLACK

  def is_start(self):
    return self.color == BLUE

  def is_end(self):
    return self.color == RED
  
  def is_empty_path(self):
    return self.color == WHITE
  
  def is_path(self):
    return self.color == GREEN

  def make_barrier(self):
    self.color = BLACK
  
  def make_start(self):
    self.color = BLUE
  
  def make_end(self):
    self.color = RED
  
  def make_path(self):
    self.color = GREEN

  def searching(self):
    self.color = GREY
  
  def reset(self):
    self.color = WHITE
  
  def update_neighbor(self, grid):
    """
    Store all neighbors spot that are path and ignore all the barriers.
    """
    if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  #Down
      self.neighbors.append(grid[self.row + 1][self.col])

    if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  #Up
      self.neighbors.append(grid[self.row - 1][self.col])

    if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #Right
      self.neighbors.append(grid[self.row][self.col + 1])
    
    if self.row > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
      self.neighbors.append(grid[self.row][self.col - 1])


  def draw(self, win):
    """
    Draw each spot.
    """
    pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


# bfs
def algorithm(draw, grid, start, end):

  marked = []
  edge_to = []
  open_set = {}
  count = 0
  # Setup some variables for the algorithm
  for row in grid:
    for spot in row:
      open_set[count] = spot
      marked.append(False)
      edge_to.append([])
      count = count + 1
  
  # This algorithm is using queue as its datastructure and we import it from build-in library.
  q = Queue()
  q.put(start)
  marked[get_key(open_set, start)] = True

  while not q.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
     
    v = q.get()

    ##
    # Visit each spot that hasn't visited yet and mark them as visited. Continue until we reach
    # our destination.
    # We store the path that we get to each spot in edge_to array for path construction.
    ##
    for w in v.neighbors:
      if not marked[get_key(open_set, w)]:
        q.put(w)
        marked[get_key(open_set, w)] = True
        edge_to[get_key(open_set, w)] = v
        w.searching()

      if w == end:
        path = path_to(marked, open_set, end, start, edge_to).first
        path_construction(path, draw, end)
        end.make_end()
        return True
    
    draw()

# If it is a path to our destination, we change the spot's color to green to resemble path.
def path_construction(path, draw, end):
  while(path.item != None):
    if path.item == end:
      break
    path.item.make_path()
    path = path.next
    draw()
      

def has_path_to(marked, dic, val):
  return marked[get_key(dic, val)]

# If there are path to our destination, we put a path that we get to destination in stack datastructure
# and construct it.
def path_to(marked, dic, val, start, edge_to):
  if not has_path_to(marked, dic, val):
    return None

  path = LinkedStackOfStrings()
  x = val

  while x != start:
    path.push(x)
    x = edge_to[get_key(dic, x)]
  return path

# Draw function ------------------------------------------------------------------------------------

def make_grid(rows, width):
  grid = []
  gap = width // rows
  for i in range(rows):
    grid.append([])
    for j in range(rows):
      spot = Node(i, j, gap, rows)
      grid[i].append(spot)
  return grid

def draw_grid(win, rows, width):
  gap = width//rows
  for i in range(rows):
    pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
      pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
    
def draw(win, grid, rows, width):
  for row in grid:
    for spot in row:
      if spot.col == 0 or spot.row == 0 or spot.col == rows-1 or spot.row == rows-1:
        spot.make_barrier()
      spot.draw(win)
    
  draw_grid(win, rows, width)
  pygame.display.update()

# End of Draw function ------------------------------------------------------------------------------------

def get_clicked_pos(pos, rows, width):
  gap = width // rows
  y, x = pos

  row = y // gap
  col = x // gap
  return row, col

def main(win, width):
  ROWS = 20
  grid = make_grid(ROWS, width)

  start = None
  end = None
  run = True
  started = False
  
  while(run):
    draw(win, grid, ROWS, width)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if started:
        continue

      if pygame.mouse.get_pressed()[0]: #Left mouse click
        pos = pygame.mouse.get_pos()
        row, col = get_clicked_pos(pos, ROWS, width)
        spot = grid[row][col]
        if not start and spot != end and not spot.is_barrier():
          start = spot
          start.make_start()
        
        elif not end and spot != start and not spot.is_barrier():
          end = spot
          end.make_end()
        
        elif spot != end and spot != start:
          spot.make_barrier()
      
      elif pygame.mouse.get_pressed()[2]: #Right mouse click
        pos = pygame.mouse.get_pos()
        row, col = get_clicked_pos(pos, ROWS, width)
        spot = grid[row][col]

        if spot == start:
          start = None
          spot.reset()
      
        elif spot == end:
          end = None
          spot.reset()
        
        spot.reset()
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and not started:
          for row in grid:
            for spot in row:
              spot.update_neighbor(grid)
          
          algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
        
        if event.key == pygame.K_c:
          start = None
          end = None
          grid = make_grid(ROWS, width)
          

  pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)