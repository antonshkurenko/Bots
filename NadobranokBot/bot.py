import tweepy
import random
import time as main_time  # do smth with two same imports
from datetime import datetime, time
from .keys import *

# ====== Constants =============================================

MY_BOT_ID = '713127255455756289'
MY_ID = '248120243'

FOLLOWER_PER_PAGE = 5000

# ====== Individual bot configuration ==========================

bot_username = 'Nadobranok'

# ====== Default phrases  ======================================

good_morning = ['Good morning, %s.', 'Have a nice day, %s.', 'Good luck, %s.', 'May the Force be with you, %s.']

good_day = ['Hey, how\'s it going, %s?', 'Hope the day is good, %s!', 'Shalom, %s!', 'Bonjour, %s!', 'What\'s up, %s?']

good_night = ['Good night, %s.', 'Sweet dreams, %s!', 'Bon nuit, %s.', 'Have a pleasant evening, %s.',
              'Buenas noches, %s.', 'Nadobranok, %s!']


def create_tweet():
    now = datetime.now()
    now_time = now.time()

    print(now_time.hour)
    if time(23) <= now_time or now_time < time(8):
        return random.choice(good_night)
    elif time(8) <= now_time < time(12):
        return random.choice(good_morning)
    else:
        return random.choice(good_day)


def get_random_follower(api):
    ids = []
    for page in tweepy.Cursor(api.followers_ids,
                              user_id=MY_ID,
                              count=FOLLOWER_PER_PAGE,
                              pagination_mode='page').pages():
        ids.extend(page)
        main_time.sleep(5)

    return random.choice(ids)


def tweet(text):
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    random_user = api.get_user(user_id=get_random_follower(api))

    print(random_user.screen_name)
    print(random_user.followers_count)

    try:
        api.update_status(text % ('@' + random_user.screen_name))
    except tweepy.error.TweepError as e:
        if e.api_code == 187:
            tweet(text)
        else:
            print(str(e))


if __name__ == "__main__":
    tweet_text = create_tweet()
    tweet(tweet_text)
