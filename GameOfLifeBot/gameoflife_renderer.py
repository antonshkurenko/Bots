from PIL import Image, ImageDraw
from gameoflife_engine import GameOfLifeEngine

# todo: make renderer as class with some preferences

# Size

LIFE_WIDTH_IN_CELLS = 20
LIFE_HEIGHT_IN_CELLS = 20

BORDER_WIDTH = 1
CELL_SIZE = 7

CELL_PLUS_BORDER = CELL_SIZE + BORDER_WIDTH

IMAGE_WIDTH = LIFE_WIDTH_IN_CELLS * CELL_SIZE + BORDER_WIDTH * (LIFE_WIDTH_IN_CELLS + 1)
IMAGE_HEIGHT = LIFE_HEIGHT_IN_CELLS * CELL_SIZE + BORDER_WIDTH * (LIFE_HEIGHT_IN_CELLS + 1)


# Colors

def color(r=0, g=0, b=0):
    return int('%02x%02x%02x' % (r, g, b), 16)


COLOR_EMPTY = color(255, 255, 255)
COLOR_FILLED = color()
COLOR_BORDER = color(100, 100, 100)


def draw_grid(canvas, size):
    # draw vertical lines
    for x in range(0, size[0], CELL_SIZE + 1):
        canvas.line((x, 0, x, size[1]), fill=COLOR_BORDER, width=BORDER_WIDTH)

    # draw horizontal lines
    for y in range(0, size[1], CELL_SIZE + 1):
        canvas.line((0, y, size[0], y), fill=COLOR_BORDER, width=BORDER_WIDTH)


def draw(canvas, life_state):
    for i in range(0, len(life_state)):
        for j in range(0, len(life_state[i])):
            if life_state[i][j] == GameOfLifeEngine.CELL_DEAD:
                pass
            elif life_state[i][j] == GameOfLifeEngine.CELL_ALIVE:
                x = i * CELL_PLUS_BORDER
                y = j * CELL_PLUS_BORDER
                canvas.rectangle((x + BORDER_WIDTH, y + BORDER_WIDTH, x + CELL_SIZE, y + CELL_SIZE), fill=COLOR_FILLED)


def save_state(filename, state):
    im = Image.new(mode='RGB', size=(IMAGE_WIDTH, IMAGE_HEIGHT), color=COLOR_EMPTY)

    canvas = ImageDraw.Draw(im)

    draw_grid(canvas, im.size)
    draw(canvas, state)

    im.save("%s.png" % filename, "PNG")

