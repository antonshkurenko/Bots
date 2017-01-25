import random


class GameOfLifeEngine:
    CELL_ALIVE = 1
    CELL_DEAD = 0

    def __init__(self, width, height, renderer):
        self.width = width
        self.height = height
        self.map = [[GameOfLifeEngine.CELL_ALIVE if random.random() < 0.33 else GameOfLifeEngine.CELL_DEAD for _ in
                     range(0, width)] for _ in range(0, height)]

        self.renderer = renderer

    def step(self):
        self.renderer.save_state('temp', self)
