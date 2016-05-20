import random

X = 1
O = -1
SPACE = 0

SIZE = 3

ROW = 'row'
COL = 'col'
DIAG = 'diag'
ANTI_DIAG = 'antidiag'
deck = [[0 for i in range(SIZE)] for i in range(SIZE)]

row = []  # SIZE
col = []  # SIZE
diag = 0
anti_diag = 0

first_bot = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

selected = Point(0, 0)

def init():
    for i in range(0, SIZE):
        row[i] = 0
        col[i] = 0
        for j in range(0, SIZE):
            deck[i][j] = SPACE

    global first_bot
    first_bot = random.choice([True, False])


def draw():
    for i in range(0, SIZE):
        for j in range(0, SIZE):

            if deck[i][j] == SPACE:
                # set char space
                pass
            elif deck[i][j] == X:
                # set char X
                pass
            elif deck[i][j] == O:
                # set char O
                pass

                # set \n


def step(x, y):

    inc = 1 if first_bot else -1

    col[x] += inc
    row[y] += inc

    global diag, anti_diag
    if x == y:
        diag += inc

    if y == SIZE - x - 1:
        anti_diag += inc


def check_sequence(x, y, length):

    if row[y] == length or row[y] == -length:
        return ROW, y

    if col[x] == length or col[x] == -length:
        return COL, x

    if diag == length or diag == -length:
        return DIAG, 0

    if anti_diag == length or anti_diag == -length:
        return ANTI_DIAG, 0

    return None


def get_space_coords():

    point = None

    for i in range(0, SIZE):
        for j in range(0, SIZE):
            if deck[i][j] == SPACE:
                flag = random.randint(0, 2)  # [0,2] -> 0,1,2

                if point is None or not flag:
                    point = Point(i, j)

    return point  # if it's none -> no free space on the deck


def get_step_point():

    for i in range(0, SIZE):
        if abs(row[i]) == SIZE - 1:
            for j in range(0, SIZE):
                if deck[j][i] == SPACE:
                    return Point(j, i)

        if abs(col[i]) == SIZE - 1:
            for j in range(0, SIZE):
                if deck[i][j] == SPACE:
                    return Point(i, j)

    if abs(diag) == SIZE - 1:
        for i in range(0, SIZE):
            if deck[i][i] == SPACE:
                return Point(i, i)

    if abs(anti_diag) == SIZE - 1:
        i = 0
        j = SIZE - 1
        while i < SIZE and j >= 0:

            if deck[i][j] == SPACE:
                return Point(i, j)

            i += 1
            j -= 1

    return get_space_coords()


def computer_step():

    step_point = get_step_point()

    deck[step_point.x][step_point.y] = 0
    step(step_point.x, step_point.y)

    win = check_sequence(step_point.x, step_point.y, SIZE)

    return win is not None


def start():

    while True:
        if first_bot:
            win = computer_step()  # first computer step
        else:
            win = computer_step()  # second computer step

        if win:
            if first_bot:
                # first bot won
                pass
            else:
                # second bot won
                pass
            break
        else:
            if get_space_coords() is None:
                # draw
                break

            global first_bot
            first_bot = not first_bot
