from KasparHauserBot.kasparhauser import KasparHauser
from KasparHauserBot.keys import BOT_KEY

def main():

    kaspar = KasparHauser(BOT_KEY)
    kaspar.start()


if __name__ == '__main__':
    main()
