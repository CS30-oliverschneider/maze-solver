import pygame
import random
import sys
import threading
import time
from operator import attrgetter

cell_size = 4
grid = (199, 199)
time_delay = 0
wait_num = 10000
start_cell = None
goal_cell = None

cells = []
running = True
display_size = (
    grid[0] * cell_size + cell_size * 2,
    grid[1] * cell_size + cell_size * 2,
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

        self.f = 0
        self.g = 0
        self.h = 0

    def __str__(self):
        return str(vars(self))

    def update_color(self):
        if self.index == 0:
            self.color = "blue"
        else:
            self.color = (
                100,
                255,
                255,
            )

    def draw(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, cell_size, cell_size))


def create_cells():
    for y in range(cell_size, grid[1] * cell_size + cell_size, cell_size):
        for x in range(cell_size, grid[0] * cell_size + cell_size, cell_size):
            if (x / cell_size) % 2 == 0 or (y / cell_size) % 2 == 0:
                cells.append(None)
                continue

            index = coords_to_index(x, y)
            cells.append(Cell(x, y, index))


def find_neighbours(cell, cell_spacing):
    neighbours = []

    left = cell_size
    right = display_size[0] - cell_size
    top = cell_size
    bottom = display_size[1] - cell_size

    def add_neighbour(index):
        if cells[index] != None and not getattr(cells[index], "visited", False):
            neighbours.append(cells[index])

    if cell.x - cell_spacing * cell_size >= left:
        add_neighbour(int(cell.index - cell_spacing))

    if cell.x + cell_spacing * cell_size < right:
        add_neighbour(int(cell.index + cell_spacing))

    if cell.y - cell_spacing * cell_size >= top:
        add_neighbour(int(cell.index - grid[0] * cell_spacing))

    if cell.y + cell_spacing * cell_size < bottom:
        add_neighbour(int(cell.index + grid[0] * cell_spacing))

    return neighbours


def coords_to_index(x, y):
    return int((x / cell_size - 1) + grid[0] * (y / cell_size - 1))


def depth_first_search():
    cell_stack = []

    start_cell.visited = True
    cell_stack.append(start_cell)

    while len(cell_stack) > 0:
        current_cell = cell_stack.pop()
        current_cell.color = "red"
        neighbours = find_neighbours(current_cell, 2)

        if time_delay > 0:
            time.sleep(time_delay)
        elif wait_num > 0:
            wait()

        current_cell.color = "white"

        if len(neighbours) == 0:
            continue

        cell_stack.append(current_cell)

        random_index = random.randrange(len(neighbours))
        random_cell = neighbours[random_index]

        x = int(current_cell.x + (random_cell.x - current_cell.x) / 2)
        y = int(current_cell.y + (random_cell.y - current_cell.y) / 2)
        index = coords_to_index(x, y)

        cells[index] = Cell(x, y, index)

        random_cell.visited = True
        cell_stack.append(random_cell)

    for cell in cells:
        if cell != None:
            del cell.visited


def a_star():
    open_list = [start_cell]
    closed_list = []

    while len(open_list) > 0:
        current_cell = min(open_list, key=attrgetter("f"))
        open_list.remove(current_cell)
        closed_list.append(current_cell)
        current_cell.color = "red"

        if same_position(current_cell, goal_cell):
            return

        neighbours = find_neighbours(current_cell, 1)
        for neighbour in neighbours:
            if neighbour in closed_list:
                continue

            neighbour.g = current_cell.g + 1
            neighbour.h = compute_h(neighbour)
            neighbour.f = neighbour.g + neighbour.h
            neighbour.parent = current_cell
            neighbour.update_color()

            for open_cell in open_list:
                if same_position(neighbour, open_cell) and neighbour.g > open_cell.g:
                    continue

            open_list.append(neighbour)

        if time_delay > 0:
            time.sleep(time_delay)
        elif wait_num > 0:
            wait()

        current_cell.update_color()


def compute_h(source):
    return abs(source.x - goal_cell.x) + abs(source.y - goal_cell.y)


def trace_path():
    current_cell = goal_cell

    while current_cell.index > 1:
        current_cell = current_cell.parent

        if current_cell.index > 0:
            current_cell.color = "yellow"

        if time_delay > 0:
            time.sleep(time_delay)
        elif wait_num > 0:
            wait()


def same_position(cell1, cell2):
    if (cell1.x, cell1.y) == (cell2.x, cell2.y):
        return True
    else:
        return False


def thread_target():
    global start_cell
    global goal_cell

    create_cells()
    start_cell = cells[0]
    goal_cell = cells[len(cells) - 1]

    depth_first_search()
    a_star()
    trace_path()


def wait():
    for _ in range(wait_num):
        pass


thread = threading.Thread(target=thread_target, daemon=True)
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
