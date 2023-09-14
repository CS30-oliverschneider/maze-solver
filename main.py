import pygame
import random
import sys
import threading
import time
import copy
from operator import attrgetter

cell_size = 10
grid = (10, 10)
time_delay = 0.001

cells = []
running = True
display_size = (
    grid[0] * cell_size * 2 + cell_size,
    grid[1] * cell_size * 2 + cell_size,
)

# Initialize pygame
pygame.init()
surface = pygame.display.set_mode(display_size)


class Cell:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.size = cell_size
        self.color = "white"
        self.index = index
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
    for y in range(cell_size, grid[1] * cell_size * 2, cell_size):
        for x in range(cell_size, grid[0] * cell_size * 2, cell_size):
            if (x / cell_size) % 2 == 0 or (y / cell_size) % 2 == 0:
                cells.append(None)
                continue

            index = coords_to_index(x, y)
            cells.append(Cell(x, y, index))


def find_neighbours(cell, cell_spacing):
    neighbours = []
    index_spacing = cell_spacing / cell_size

    left = cell_size
    right = display_size[0] - cell_size
    top = cell_size
    bottom = display_size[1] - cell_size

    def add_neighbour(index):
        if cells[index] != None and not cells[index].visited:
            neighbours.append(cells[index])

    if cell.x - cell_spacing >= left:
        add_neighbour(int(cell.index - index_spacing))

    if cell.x + cell_spacing <= right:
        add_neighbour(int(cell.index + index_spacing))

    if cell.y - cell_spacing >= top:
        add_neighbour(int(cell.index - grid[0] * index_spacing))

    if cell.y + cell_spacing <= bottom:
        add_neighbour(int(cell.index + grid[0] * index_spacing))

    return neighbours


def coords_to_index(x, y):
    return int(((x - cell_size) / cell_size) * ((y - cell_size) / cell_size))


def depth_first_search(initial_cell):
    cell_stack = []

    initial_cell.visited = True
    cell_stack.append(initial_cell)

    while len(cell_stack) > 0:
        current_cell = cell_stack.pop()
        neighbours = find_neighbours(current_cell, 2 * cell_size)

        if len(neighbours) == 0:
            continue

        cell_stack.append(current_cell)

        random_index = random.randrange(len(neighbours))
        random_cell = neighbours[random_index]

        x = current_cell.x + (random_cell.x - current_cell.x) / 2
        y = current_cell.y + (random_cell.y - current_cell.y) / 2
        index = coords_to_index(x, y)
        cells[index] = Cell(x, y, index)

        random_cell.visited = True
        cell_stack.append(random_cell)

        if time_delay > 0:
            time.sleep(time_delay)


def a_star(initial_cell):
    initial_cell.f = 0
    open_list = [initial_cell]
    closed_list = []

    while len(open_list) > 0:
        smallest_f = min(open_list, key=attrgetter("f"))
        open_list.remove(smallest_f)


def thread_target():
    create_cells()
    depth_first_search(cells[0])
    # a_star(cells[0])


thread = threading.Thread(target=thread_target)
thread.daemon = True
thread.start()


# Program Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for cell in cells:
        if cell != None:
            cell.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
