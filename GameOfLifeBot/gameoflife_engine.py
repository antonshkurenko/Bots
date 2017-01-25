import random
from utils import read_file, split_str_to_ints, write_matrix_to_file


class GameOfLifeEngine:
    CELL_ALIVE = 1
    CELL_DEAD = 0

    HISTORY_LIMIT = 10

    def __init__(self, renderer, **kwargs):

        if 'filename' in kwargs:
            self.__init_from_file(kwargs.pop('filename'))
        elif 'width' in kwargs and 'height' in kwargs:
            self.__init_from_args(kwargs.pop('width'), kwargs.pop('height'))
        else:
            raise TypeError('Provide filename or width + height')

        self.renderer = renderer

    def step(self):

        self.__life()

        self.renderer.draw_state('temp', self)
        self.__save_to_file('temp_file2.txt')

    def __init_from_args(self, width, height):
        self.width = width
        self.height = height
        self.map = [[GameOfLifeEngine.CELL_ALIVE if random.random() < 0.33 else GameOfLifeEngine.CELL_DEAD for _ in
                     range(0, width)] for _ in range(0, height)]

        self.history = []

    def __init_from_file(self, filename):
        lines = read_file(filename)
        self.width, self.height = split_str_to_ints(lines[0])

        self.map = []
        self.history = []

        # current state
        for i in range(1, self.height + 1):
            self.map.append(split_str_to_ints(lines[i]))

        for i in range(self.height + 1, len(lines), self.height):

            history_step = []

            for j in range(0, self.height):
                print('j = %s, i = %s, i + j = %s' % (j, i, i + j))
                history_step.append(split_str_to_ints(lines[i + j]))

            self.history.append(history_step)

    def __life(self):
        pass

    def __save_to_file(self, filename):
        file = open(filename, 'w+')

        file.write('%s %s\n' % (self.width, self.height))

        # todo write actual result and history

        write_matrix_to_file(file, self.map)

        limit = min(GameOfLifeEngine.HISTORY_LIMIT, len(self.history))

        for i in range(0, limit):
            write_matrix_to_file(file, self.history[i])
