import logging
from google_search import GoogleSearch
from kasparhauser import KasparHauser
from keys import BOT_KEY, GOOGLE_KEY, GOOGLE_SEARCH_ENGINE_ID

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                  level=logging.INFO)

def main():

    kaspar = KasparHauser(BOT_KEY, GoogleSearch(GOOGLE_KEY, GOOGLE_SEARCH_ENGINE_ID))

    logging.log(logging.DEBUG, 'Kaspar Hauser will be started now')

    kaspar.start()


if __name__ == '__main__':
    main()
