import random
import time

X = 1
O = -1
SPACE = 0

SIZE = 3

ROW = 'row'
COL = 'col'
DIAG = 'diag'
ANTI_DIAG = 'antidiag'
deck = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

row = [0 for _ in range(SIZE)]  # SIZE
col = [0 for _ in range(SIZE)]  # SIZE
diag = 0
anti_diag = 0

first_bot = False
selected = 0, 0


def init():

    print('init')

    for i in range(0, SIZE):
        row[i] = 0
        col[i] = 0
        for j in range(0, SIZE):
            deck[i][j] = SPACE

    global first_bot
    first_bot = random.choice([True, False])


def draw():

    print('draw')

    for i in range(0, SIZE):
        for j in range(0, SIZE):

            if deck[i][j] == SPACE:
                # set char space
                print('.', end='')
                pass
            elif deck[i][j] == X:
                # set char X
                print('X', end='')
                pass
            elif deck[i][j] == O:
                # set char O
                print('O', end='')
                pass
        print()
        # set \n


def step(x, y):

    print('step')

    inc = 1 if first_bot else -1

    col[x] += inc
    row[y] += inc

    global diag, anti_diag
    if x == y:
        diag += inc

    if y == SIZE - x - 1:
        anti_diag += inc


def check_sequence(x, y, length):

    print('check sequence')

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

    print('get space coords')

    point = None

    for i in range(0, SIZE):
        for j in range(0, SIZE):
            if deck[i][j] == SPACE:
                flag = random.randint(0, 2)  # [0,2] -> 0,1,2

                if point is None or not flag:
                    point = i, j

    return point  # if it's none -> no free space on the deck


def get_step_point():

    print('get step point')

    for i in range(0, SIZE):
        if abs(row[i]) == SIZE - 1:
            for j in range(0, SIZE):
                if deck[j][i] == SPACE:
                    return j, i

        if abs(col[i]) == SIZE - 1:
            for j in range(0, SIZE):
                if deck[i][j] == SPACE:
                    return i, j

    if abs(diag) == SIZE - 1:
        for i in range(0, SIZE):
            if deck[i][i] == SPACE:
                return i, i

    if abs(anti_diag) == SIZE - 1:
        i = 0
        j = SIZE - 1
        while i < SIZE and j >= 0:

            if deck[i][j] == SPACE:
                return i, j

            i += 1
            j -= 1

    return get_space_coords()


def computer_step():

    print('computer_step')

    step_point = get_step_point()

    deck[step_point[0]][step_point[1]] = O if first_bot else X

    win = check_sequence(step_point[0], step_point[1], SIZE)

    return win is not None


def start():

    print('start')

    init()

    while True:

        if first_bot:
            print('first computer step')
            win = computer_step()  # first computer step
        else:
            print('second computer step')
            win = computer_step()  # second computer step

        draw()

        if win:
            if first_bot:
                # first bot won
                print('first computer won')
                pass
            else:
                # second bot won
                print('second computer won')
                pass
            break
        else:
            if get_space_coords() is None:
                # draw
                print('draw')
                break

            global first_bot
            first_bot = not first_bot

        time.sleep(5)
        print('****** NEXT ******')

