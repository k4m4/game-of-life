import pygame
from pygame import Vector2, Rect

VIEW_W = VIEW_H = 720
MODEL_W = MODEL_H = 100
FPS = 60
SPEED = 5

pygame.init()
screen = pygame.display.set_mode((VIEW_W, VIEW_H))
clock = pygame.time.Clock()
running = True

glider_pattern = {
    (1, 0),
    (2, 1),
    (0, 2),
    (1, 2),
    (2, 2),
}

gosper_glider_gun = {
    (1, 5), (1, 6), (2, 5), (2, 6), (11, 5), (11, 6), (11, 7), (12, 4), (12, 8),
    (13, 3), (13, 9), (14, 3), (14, 9), (15, 6), (16, 4), (16, 8), (17, 5),
    (17, 6), (17, 7), (18, 6), (21, 3), (21, 4), (21, 5), (22, 3), (22, 4),
    (22, 5), (23, 2), (23, 6), (25, 1), (25, 2), (25, 6), (25, 7), (35, 3),
    (35, 4), (36, 3), (36, 4)
}

population = gosper_glider_gun

class ModelToView:
    @classmethod
    def position(cls, r):
        x, y = r
        return Vector2(x * VIEW_W / MODEL_W + VIEW_W / 2, VIEW_H / 2 - y * VIEW_H / MODEL_H)

    @classmethod
    def size(cls, r):
        x, y = r
        return Vector2(x * VIEW_W / MODEL_W, y * VIEW_H / MODEL_H)

    @classmethod
    def rect(cls, rect):
        return Rect(cls.position(rect.topleft), cls.size(rect.size))

def render_population():
    for x, y in population:
        rect = Rect(x, y, 1, 1)
        pygame.draw.rect(screen, "black", ModelToView.rect(rect))

def neighbors(citizen):
    x, y = citizen
    potential_neigbors = set(((x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)))
    return potential_neigbors

def count_alive_neighbors(citizen):
    return len(population & neighbors(citizen))

def grow(population):
    return population | set().union(*(neighbors((x, y)) for x, y in population))

def evolve(population):
    new_population = set()
    for x, y in grow(population):
        num_of_alive_neighbors = count_alive_neighbors((x, y))
        if (x, y) in population and num_of_alive_neighbors == 2 or num_of_alive_neighbors == 3:
            new_population.add((x, y))
    return new_population

tick_count = 1
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    render_population()
    if tick_count % SPEED == 0:
        population = evolve(population)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to 60
    tick_count += 1

pygame.quit()
