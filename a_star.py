from queue import PriorityQueue
import math
import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)
ORANGE = (255, 165 ,0)
GREY = (127, 127, 127)
PURPLE = (128, 0, 128)
TURQUOISE = (64, 224, 208)


WIDTH = 800

WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


class Node:
    """ Class representing node in graph/cell. Used to visualize A* pathfinding algorithm using python module pygame. """
    
    
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.color == BLACK

    def is_visited(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN
    
    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_wall(self):
        self.color = BLACK
    
    def reset(self):
        self.color = WHITE

    def make_path(self):
        self.color = PURPLE
    
    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False




# Manhatan distance
def h(p1, p2): 
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstructPath(cameFrom, current, draw):
    while current in cameFrom.keys():
        current = cameFrom[current]
        current.make_path()
        draw()

def a_star(draw, start, grid, goal):
    """ A* path finding algorithm """
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    cameFrom = {}
    gScore = {node : float("inf") for row in grid for node in row}
    gScore[start] = 0  
    fScore = {node : float("inf") for row in grid for node in row}
    fScore[start] = h(start.get_pos(), goal.get_pos())

    hashSet = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        hashSet.remove(current)


        if current == goal:
            reconstructPath(cameFrom, current, draw)
            goal.make_end()
            return True

        for neighbor in current.neighbors:
            tmp_gScore = gScore[current] + 1

            if tmp_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tmp_gScore
                fScore[neighbor] = gScore[neighbor] + h(neighbor.get_pos(), goal.get_pos())
                if neighbor not in hashSet:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    hashSet.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()
    
    return False



def make_grid(width, rows):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
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

def get_clicked_node(pos, width, rows):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col



def main(window, width):
    ROWS = 50
    grid = make_grid(width, ROWS)

    start = None
    stop = None


    run = True

    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node(pos, width, ROWS)
                node = grid[row][col]
                if not start and node != stop:
                    start = node
                    start.make_start()
                elif not stop and node != start:
                    stop = node
                    stop.make_end()
                elif node != start and node != stop:
                    node.make_wall()
                
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node(pos, width, ROWS)
                node = grid[row][col]
                if node == start:
                    start = None
                elif node == stop:
                    stop = None
                else:
                    node.reset()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and stop:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                
                    a_star(lambda: draw(window, grid, ROWS, width), start, grid, stop)
                
                elif event.key == pygame.K_n:
                    start = None
                    stop = None
                    for row in grid:
                        for node in row:
                            
                            node.reset()

    pygame.quit()



if __name__ == "__main__":
    main(WINDOW, WIDTH)