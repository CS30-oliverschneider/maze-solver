import pygame
import random
import sys

cell_size = 50
display_size = (350, 350)
running = True
cells = []
frames_per_step = 50
grid = (
    (display_size[0] - cell_size) / cell_size / 2, 
    (display_size[1] - cell_size) / cell_size / 2
)

# Initialize pygame
pygame.init()
surface = pygame.display.set_mode(display_size)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = cell_size
        self.index = len(cells)
        self.visited = False

        self.left = True
        self.right = True
        self.top = True
        self.bottom = True

        cells.append(self)

    def __str__(self):
        return str(vars(self))

    def draw(self):
        pygame.draw.rect(surface, "white", (self.x, self.y, cell_size, cell_size))


def create_cells():
    for y in range(cell_size, display_size[1], cell_size * 2):
        for x in range(cell_size, display_size[0], cell_size * 2):
            Cell(x, y)


def depth_first_search(cell):
    initial_cells = cells.copy()
    neighbours = []

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

    print(cell.index, len(neighbours))

    if len(neighbours) == 0:
        return

    random_indexes = list(range(len(neighbours)))
    random.shuffle(random_indexes)

    for index in random_indexes:
        random_cell = neighbours[index]
        if random_cell.visited:
            return
        
        random_cell.visited = True
        Cell(cell.x + (random_cell.x - cell.x) / 2, cell.y + (random_cell.y - cell.y) / 2)
        depth_first_search(random_cell)


create_cells()
depth_first_search(cells[0])


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