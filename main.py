import pygame
import random
import sys
import threading
import time
import copy

cell_size = 10
grid = (40, 40)
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
            cells.append(Cell(x, y))


def depth_first_search(initial_cell):
    initial_cells = copy.deepcopy(cells)
    cell_stack = []

    initial_cell.visited = True
    cell_stack.append(initial_cell)

    while len(cell_stack) > 0:
        current_cell = cell_stack.pop()
        neighbours = []

        def add_neighbour(index):
            if not initial_cells[index].visited:
                neighbours.append(initial_cells[index])

        if current_cell.x - cell_size >= initial_cells[0].x:
            add_neighbour(int(current_cell.index - 1))

        if current_cell.x + cell_size <= initial_cells[len(initial_cells) - 1].x:
            add_neighbour(int(current_cell.index + 1))

        if current_cell.y - cell_size >= initial_cells[0].y:
            add_neighbour(int(current_cell.index - grid[0]))

        if current_cell.y + cell_size <= initial_cells[len(initial_cells) - 1].y:
            add_neighbour(int(current_cell.index + grid[0]))

        if len(neighbours) == 0:
            continue

        cell_stack.append(current_cell)

        random_index = random.randrange(len(neighbours))
        random_cell = neighbours[random_index]

        x = current_cell.x + (random_cell.x - current_cell.x) / 2
        y = current_cell.y + (random_cell.y - current_cell.y) / 2
        cells.append(Cell(x, y))

        random_cell.visited = True
        cell_stack.append(random_cell)

        # time.sleep(time_delay)


def a_star(initial_cell):
    initial_cell.f = 0
    open_list = [initial_cell]
    closed_list = []

    while len(open_list) > 0:
        q_index = "something"


def thread_target():
    create_cells()
    depth_first_search(cells[0])
    a_star(cells[0])


thread = threading.Thread(target=thread_target)
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
