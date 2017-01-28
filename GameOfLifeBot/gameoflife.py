import os.path
from gameoflife_engine import GameOfLifeEngine
from gameoflife_renderer import GameOfLifeRenderer


def main():
    filename = 'history.txt'
    pic_filename = 'current_state.png'

    if os.path.exists(filename):
        gof = GameOfLifeEngine(GameOfLifeRenderer(), filename=filename)
        life_continues = gof.step()
    else:
        gof = GameOfLifeEngine(GameOfLifeRenderer(), width=15, height=15)
        life_continues = True

    gof.save(filename, pic_filename, life_continues)

if __name__ == '__main__':
    main()
