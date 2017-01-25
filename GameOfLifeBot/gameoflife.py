import gameoflife_renderer
from gameoflife_engine import GameOfLifeEngine


def main():

    gof = GameOfLifeEngine(10, 10)
    print(gof.__dict__)


if __name__ == '__main__':
    main()