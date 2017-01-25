import gameoflife_renderer
from gameoflife_engine import GameOfLifeEngine
from gameoflife_renderer import GameOfLifeRenderer


def main():
    gof = GameOfLifeEngine(GameOfLifeRenderer(), filename='temp_file.txt')
    print(gof.__dict__)
    gof.step()


if __name__ == '__main__':
    main()
