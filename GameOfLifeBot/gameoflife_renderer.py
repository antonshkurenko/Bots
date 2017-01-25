from PIL import Image, ImageDraw
from gameoflife_engine import GameOfLifeEngine
from utils import color


class GameOfLifeRenderer:

    def __init__(self, **kwargs):
        self.border_width = kwargs.pop('border_width', 1)
        self.cell_size = kwargs.pop('cell_size', 7)

        self.color_empty = kwargs.pop('color_empty', color(255, 255, 255))
        self.color_filled = kwargs.pop('color_filled', color())
        self.color_border = kwargs.pop('color_border', color(100, 100, 100))

        self.cell_plus_border = self.border_width + self.cell_size

    def __draw(self, canvas, life_state):

        for i in range(0, len(life_state)):
            for j in range(0, len(life_state[i])):
                if life_state[i][j] == GameOfLifeEngine.CELL_DEAD:
                    pass
                elif life_state[i][j] == GameOfLifeEngine.CELL_ALIVE:
                    x = i * self.cell_plus_border
                    y = j * self.cell_plus_border
                    canvas.rectangle(
                        (x + self.border_width, y + self.border_width, x + self.cell_size, y + self.cell_size),
                        fill=self.color_filled)

    def __draw_grid(self, canvas, size):
        # draw vertical lines
        for x in range(0, size[0], self.cell_size + 1):
            canvas.line((x, 0, x, size[1]), fill=self.color_border, width=self.border_width)

        # draw horizontal lines
        for y in range(0, size[1], self.cell_size + 1):
            canvas.line((0, y, size[0], y), fill=self.color_border, width=self.border_width)

    def save_state(self, filename, state):

        height_in_cells = len(state)
        width_in_cells = len(state[0])  # hope all lines have equal sizes

        image_width = width_in_cells * self.cell_size + self.border_width * (width_in_cells + 1)
        image_height = height_in_cells * self.cell_size + self.border_width * (height_in_cells + 1)

        im = Image.new(mode='RGB', size=(image_width, image_height), color=self.color_empty)

        canvas = ImageDraw.Draw(im)

        self.__draw_grid(canvas, im.size)
        self.__draw(canvas, state)

        im.save("%s.png" % filename, "PNG")
