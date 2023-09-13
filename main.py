import pygame
import random
import sys
import threading
import time

cell_size = 10
grid = (40, 40)
time_delay = 0.001

running = True
initial_cells = []
cells = []
display_size = (
    grid[0] * cell_size * 2 + cell_size,
    grid[1] * cell_size * 2 + cell_size,
)

# Initialize pygame
pygame.init()
surface = pygame.display.set_mode(display_size)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = cell_size
        self.color = "white"
        self.index = len(cells)
        self.visited = False

        self.left = True
        self.right = True
        self.top = True
        self.bottom = True

    def __str__(self):
        return str(vars(self))

    def draw(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, cell_size, cell_size))


def create_cells():
    for y in range(cell_size, grid[1] * cell_size * 2 + cell_size, 2 * cell_size):
        for x in range(cell_size, grid[0] * cell_size * 2 + cell_size, 2 * cell_size):
            cell = Cell(x, y)
            initial_cells.append(cell)
            cells.append(cell)


def depth_first_search(cell):
    neighbours = []
    cell.visited = True

    def add_cell(index):
        if not initial_cells[index].visited:
            neighbours.append(initial_cells[index])

    if cell.x - cell_size >= initial_cells[0].x:
        add_cell(int(cell.index - 1))

    if cell.x + cell_size <= initial_cells[len(initial_cells) - 1].x:
        add_cell(int(cell.index + 1))

    if cell.y - cell_size >= initial_cells[0].y:
        add_cell(int(cell.index - grid[0]))

    if cell.y + cell_size <= initial_cells[len(initial_cells) - 1].y:
        add_cell(int(cell.index + grid[0]))

    if len(neighbours) == 0:
        return

    random_indexes = list(range(len(neighbours)))
    random.shuffle(random_indexes)

    for index in random_indexes:
        random_cell = neighbours[index]
        if random_cell.visited:
            return

        x = cell.x + (random_cell.x - cell.x) / 2
        y = cell.y + (random_cell.y - cell.y) / 2
        cells.append(Cell(x, y))

        time.sleep(time_delay)
        depth_first_search(random_cell)


create_cells()

thread = threading.Thread(target=depth_first_search, args=(cells[0],))
thread.daemon = True
thread.start()


# Program Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for cell in cells:
        cell.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
