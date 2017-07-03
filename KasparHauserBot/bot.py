from kasparhauser import KasparHauser
from keys import BOT_KEY


def main():

    kaspar = KasparHauser(BOT_KEY)
    kaspar.start()


if __name__ == '__main__':
    main()
