import pygame
import sys

display_size = (850, 850)
cellSize = 50
running = True
cells = []
frames_per_step = 50

# Initialize pygame
pygame.init()
surface = pygame.display.set_mode(display_size)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = cellSize
        self.left = True
        self.right = True
        self.top = True
        self.bottom = True

        cells.append(self)

    def __str__(self):
        return str(vars(self))

    def draw(self):
        pygame.draw.rect(surface, "white", (self.x, self.y, cellSize, cellSize))


def create_cells():
    for y in range(cellSize, display_size[1], cellSize * 2):
        for x in range(cellSize, display_size[0], cellSize * 2):
            Cell(x, y)


def depth_first_search(cell):
    neighbours = []
    if cell.y - cellSize > 0:
        neighbours.push()


create_cells()


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
