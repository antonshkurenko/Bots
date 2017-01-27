import random
from utils import read_file, split_str_to_ints, write_matrix_to_file


class GameOfLifeEngine:
    CELL_ALIVE = 1
    CELL_DEAD = 0

    HISTORY_LIMIT = 100

    def __init__(self, renderer, **kwargs):

        if 'filename' in kwargs:
            self.__init_from_file(kwargs.pop('filename'))
        elif 'width' in kwargs and 'height' in kwargs:
            self.__init_from_args(kwargs.pop('width'), kwargs.pop('height'))
        else:
            raise TypeError('Provide filename or width + height')

        self.renderer = renderer

    def step(self):
        return self.__life()

    def save(self, filename, life_continues):
        import datetime
        self.renderer.draw_state(str(datetime.datetime.now()), self)

        self.__save_to_file(filename)

        if life_continues:
            pass

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

        current_state = self.map

        self.history.insert(0, current_state)
        self.map = [[GameOfLifeEngine.CELL_DEAD for _ in
                     range(0, self.width)] for _ in range(0, self.height)]

        for y in range(0, len(current_state)):
            for x in range(0, len(current_state[y])):

                neighbours_count = self.__neighbours_count(x, y, current_state)

                if neighbours_count == 3 or (
                                neighbours_count == 2 and current_state[y][x] == GameOfLifeEngine.CELL_ALIVE):
                    self.map[y][x] = GameOfLifeEngine.CELL_ALIVE

        return not (GameOfLifeEngine.__check_any_alive(self.map) or
                    GameOfLifeEngine.__check_exists_in_history(self.map, self.history))

    def __neighbours_count(self, x, y, current_state):

        count = 0

        for horizontal in [-1, 0, 1]:
            for vertical in [-1, 0, 1]:
                if not horizontal == vertical == 0:
                    count += current_state[(y + vertical) % self.height][(x + horizontal) % self.width]

        return count

    @staticmethod
    def __check_any_alive(state):
        for i in range(0, len(state)):
            for j in range(0, len(state[i])):
                if state[i][j] == GameOfLifeEngine.CELL_ALIVE:
                    return True

        return False

    @staticmethod
    def __check_exists_in_history(state, history):

        for history_state in history:
            if state == history_state:
                return True

        return False

    def __save_to_file(self, filename):
        file = open(filename, 'w+')

        file.write('%s %s\n' % (self.width, self.height))

        write_matrix_to_file(file, self.map)

        limit = min(GameOfLifeEngine.HISTORY_LIMIT, len(self.history))

        for i in range(0, limit):
            write_matrix_to_file(file, self.history[i])
