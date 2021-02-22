from queue import PriorityQueue
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)
ORANGE = (255, 165 ,0)
GREY = (127, 127, 127)


WIDTH = 800



WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


class Node:
    """ Class representing node in graph/cell. Used to visualize A* pathfinding algorithm using python module pygame. """
    
    
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = row * width
        self.color  = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))


# Manhatan distance
def h(p1, p2): 
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruckPath(cameFrom, current):
    pass

def a_star(start, grid, goal, h):
    """ A* path finding algorithm to go th """
    pass 


def make_grid(width, rows):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Node(i, j, gap, rows))
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(window, grid, rows, width):
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(window)
    
    draw_grid(window, rows, width)
    pygame.display.update()



def main(window, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    run = True

    while run :
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


if __name__ == "__main__":
    main(WINDOW, WIDTH)