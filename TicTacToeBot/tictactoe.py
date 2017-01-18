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

streak_strings = {
    3: 'Killing Spree!',
    4: 'Dominating!',
    5: 'Mega Kill!',
    6: 'Unstoppable!',
    7: 'Wicked Sick!',
    8: 'Monster Kill!',
    9: 'Godlike!',
    10: 'Beyond Godlike!'
}


def init():
    print('init')

    for i in range(0, SIZE):
        row[i] = 0
        col[i] = 0
        for j in range(0, SIZE):
            deck[i][j] = SPACE

    global first_bot
    first_bot = random.choice([True, False])


def draw(tweet_callback):
    print('draw')

    print('row:' + str(row))
    print('col:' + str(col))

    tweet_text = ''

    for i in range(0, SIZE):
        for j in range(0, SIZE):

            if deck[i][j] == SPACE:
                # set char space
                space_symbol = '−'
                # print(space_symbol, end='')
                tweet_text += space_symbol
                pass
            elif deck[i][j] == X:
                # set char X
                x_symbol = '×'
                # print(x_symbol, end='')
                tweet_text += x_symbol
                pass
            elif deck[i][j] == O:
                # set char O
                o_symbol = '○'
                # print(o_symbol, end='')
                tweet_text += o_symbol
                pass

            if j != SIZE - 1:
                print('|', end='')
                tweet_text += '|'

        # print()
        tweet_text += '\n'
        # set \n
    tweet_callback(tweet_text)


def step(x, y):
    # print('step')

    inc = 1 if first_bot else -1

    col[x] += inc
    row[y] += inc

    global diag, anti_diag
    if x == y:
        diag += inc

    if y == SIZE - x - 1:
        anti_diag += inc


def check_sequence(x, y, length):
    # print('check sequence')

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
    # print('get space coords')

    point = None

    for i in range(0, SIZE):
        for j in range(0, SIZE):
            if deck[i][j] == SPACE:
                flag = random.randint(0, 3)  # [0,3] -> 0,1,2,3 -> 25%

                if point is None or not flag:
                    point = i, j

    return point  # if it's none -> no free space on the deck


def get_step_point():
    # print('get step point')

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
    # print('computer_step')

    step_point = get_step_point()

    deck[step_point[0]][step_point[1]] = O if first_bot else X
    step(step_point[0], step_point[1])

    win = check_sequence(step_point[0], step_point[1], SIZE)

    return win is not None


def start(tweet_callback):
    # print('start')

    init()

    lines = [line.rstrip('\n') for line in open('result.txt', 'r')]

    # line 0 -> total rounds
    # line 1 -> O wins
    # line 2 -> X wins
    # line 3 -> draws
    # line 4 -> O streak
    # line 5 -> X streak
    # line 6 -> draw streak

    # print(lines)

    start_round_string = 'Round %d: FIGHT!'
    lines[0] = int(lines[0]) + 1
    tweet_callback(start_round_string % int(lines[0]))

    while True:

        if first_bot:
            # print('first computer step')
            win = computer_step()  # first computer step
        else:
            # print('second computer step')
            win = computer_step()  # second computer step

        draw(tweet_callback)

        if win:
            if first_bot:
                # first bot won
                # print('first computer won')
                result = O
            else:
                # second bot won
                # print('second computer won')
                result = X
            break
        else:
            if get_space_coords() is None:
                # draw
                # print('draw')
                result = SPACE
                break

            global first_bot
            first_bot = not first_bot

        print('*** End of the step ***')
        time.sleep(5)

    if result == O:
        lines[1] = int(lines[1]) + 1
        lines[5] = 0
        lines[6] = 0
        lines[4] = int(lines[4]) + 1

        final_tweet = 'O won!\n'

        win_streak = int(lines[4])
        if win_streak >= 3:
            streak = streak_strings.get(win_streak, 'Beyond Godlike!')
            final_tweet += streak + '\n'

    elif result == X:
        lines[2] = int(lines[2]) + 1
        lines[4] = 0
        lines[6] = 0
        lines[5] = int(lines[5]) + 1

        final_tweet = 'X won!\n'

        win_streak = int(lines[5])
        if win_streak >= 3:
            streak = streak_strings.get(win_streak, 'Beyond Godlike!')
            final_tweet += streak + '\n'

    elif result == SPACE:
        lines[3] = int(lines[3]) + 1
        lines[4] = 0
        lines[5] = 0
        lines[6] = int(lines[6]) + 1

        final_tweet = 'Draw!\n'

    final_tweet += 'O wins: %d\n' \
                   'X wins: %d\n' \
                   'Draws: %d\n' \
                   'O streak: %d\n' \
                   'X streak: %d\n' \
                   'Draw streak: %d' % \
                   (int(lines[1]),
                    int(lines[2]),
                    int(lines[3]),
                    int(lines[4]),
                    int(lines[5]),
                    int(lines[6]))

    file = open('result.txt', 'w')
    for item in lines:
        file.write("%s\n" % item)

    # print(final_tweet)
    tweet_callback(final_tweet)
