import os.path
from gameoflife_engine import GameOfLifeEngine
from gameoflife_renderer import GameOfLifeRenderer


def create_message(gof):
    return 'Generation: %s' % gof.generation


def play():
    filename = 'history.txt'
    pic_filename = 'current_state.png'

    if os.path.exists(filename):
        gof = GameOfLifeEngine(GameOfLifeRenderer(), filename=filename)
        life_continues = gof.step()
    else:
        gof = GameOfLifeEngine(GameOfLifeRenderer(), width=15, height=15)
        life_continues = True

    gof.save(filename, pic_filename, life_continues)
    return pic_filename, create_message(gof)
