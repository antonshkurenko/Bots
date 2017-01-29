import tweepy
from keys import *
from gameoflife import play

# ====== Constants =============================================

MY_BOT_ID = '825414146745331714'
MY_ID = '248120243'

# ====== Individual bot configuration ==========================

BOT_USERNAME = 'gameoflifebot'


def tweet(pic, txt):
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        api.update_with_media(pic, txt)
    except tweepy.error.TweepError as e:
        if e.api_code == 187:
            tweet(pic, txt)
        else:
            print(e)


if __name__ == '__main__':

    picture, text = play()

    tweet(picture, text)
