import os.path
from gameoflife_engine import GameOfLifeEngine
from gameoflife_renderer import GameOfLifeRenderer


def main():
    filename = 'history.txt'

    if os.path.exists(filename):
        gof = GameOfLifeEngine(GameOfLifeRenderer(), filename=filename)
        life_continues = gof.step()
    else:
        gof = GameOfLifeEngine(GameOfLifeRenderer(), width=15, height=15)
        life_continues = True

    gof.save(filename, life_continues)


if __name__ == '__main__':
    main()
