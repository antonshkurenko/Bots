import tweepy
from keys import *
from tictactoe import *

# ====== Constants =============================================

MY_BOT_ID = '733355119161577472'
MY_ID = '248120243'

# ====== Individual bot configuration ==========================

bot_username = 'BotTicTacToe'


def tweet(text):
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        if e.api_code == 187:
            tweet(text)
        else:
            print(e)


if __name__ == '__main__':
    start(tweet)
