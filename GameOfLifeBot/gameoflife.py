import gameoflife_renderer
from gameoflife_engine import GameOfLifeEngine
from gameoflife_renderer import GameOfLifeRenderer


def main():
    gof = GameOfLifeEngine(10, 10, GameOfLifeRenderer())
    gof.step()


if __name__ == '__main__':
    main()
