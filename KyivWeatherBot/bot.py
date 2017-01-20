import tweepy
from keys import *
import urllib.request
import json
import datetime
import random

# ====== Constants =============================================

MY_BOT_ID = '821783817925038080'
MY_ID = '248120243'

EMPTY_STRING = ''

STATE_DAY = 'day'
STATE_NIGHT = 'night'
STATE_SUNSET = 'sunset'
STATE_SUNRISE = 'sunrise'

SURPRISE_CHANCE = 0.2

# ====== Individual bot configuration ==========================

BOT_USERNAME = 'kyivweatherbot'

# ====== Weather icon to emoji map =============================


def is_surprise():
    """Util function, needs for emoji."""
    return random.random < SURPRISE_CHANCE


THERMOMETER_EMOJI = u'\U0001F321'
DROPLET_EMOJI = u'\U0001F4A7'

QUESTION_EMOJI = u'\U00002753'

# weather
SNOW_EMOJI = u'\U0001F328'
RAIN_EMOJI = u'\U0001F327'
RAIN_AND_STORM_EMOJI = u'\U000026C8'
TORNADO_EMOJI = u'\U0001F32A'
SUN_EMOJI = u'\U00002600'
CLOUD_EMOJI = u'\U00002601'
FOG_EMOJI = u'\U0001F32B'
FOGGY_EMOJI = u'\U0001F301'
SMALL_SUN_BIG_CLOUD = u'\U0001F325'
BIG_SUN_SMALL_CLOUD = u'\U0001F324'

# moons
NEW_MOON_EMOJI = u'\U0001F311'
WAXING_CRESCENT_MOON_EMOJI = u'\U0001F312'
FIRST_QUARTER_MOON_EMOJI = u'\U0001F313'
WAXING_GIBBOUS_MOON_EMOJI = u'\U0001F314'
FULL_MOON_EMOJI = u'\U0001F315'
WANING_GIBBOUS_MOON_EMOJI = u'\U0001F316'
LAST_QUARTER_MOON_EMOJI = u'\U0001F317'
WANING_CRESCENT_MOON_EMOJI = u'\U0001F318'

# surprises
UMBRELLA_WITH_DROPS_EMOJI = u'\U00002614'
SNOWMAN_EMOJI = u'\U00002603'
SNOWFLAKE_EMOJI = u'\U00002744'
RAINBOW_EMOJI = u'\U0001F308'
NIGHT_WITH_STARTS_EMOJI = u'\U0001F303'

RAIN_SURPRISES = [UMBRELLA_WITH_DROPS_EMOJI, RAIN_AND_STORM_EMOJI]
SNOW_SURPRISES = [SNOWMAN_EMOJI, SNOWFLAKE_EMOJI]

SUNRISE_MOUNTAINS_EMOJI = u'\U0001F304'
SUNRISE_EMOJI = u'\U0001F305'
SUNSET_EMOJI = u'\U0001F307'

WEATHER_ICON_TO_EMOJI_MAP = {
    'chanceflurries': QUESTION_EMOJI + SNOW_EMOJI + TORNADO_EMOJI,
    'chancerain': QUESTION_EMOJI + RAIN_EMOJI + random.choice(RAIN_SURPRISES) if is_surprise() else EMPTY_STRING,
    'chancesleet': QUESTION_EMOJI + SNOW_EMOJI + RAIN_EMOJI,
    'chancesnow': QUESTION_EMOJI + SNOW_EMOJI + random.choice(SNOW_SURPRISES) if is_surprise() else EMPTY_STRING,
    'chancetstorms': QUESTION_EMOJI + RAIN_AND_STORM_EMOJI,
    'clear': 'clear',  # check if it's night -> moon, day -> sun
    'cloudy': CLOUD_EMOJI,
    'flurries': SNOW_EMOJI + TORNADO_EMOJI,
    'fog': FOG_EMOJI,
    'hazy': FOGGY_EMOJI,
    'mostlycloudy': SMALL_SUN_BIG_CLOUD,
    'mostlysunny': BIG_SUN_SMALL_CLOUD,
    'partlycloudy': BIG_SUN_SMALL_CLOUD,
    'partlysunny': SMALL_SUN_BIG_CLOUD,
    'sleet': SNOW_EMOJI + RAIN_EMOJI,
    'rain': RAIN_EMOJI + random.choice(RAIN_SURPRISES) if is_surprise() else EMPTY_STRING,
    'snow': SNOW_EMOJI + random.choice(SNOW_SURPRISES) if is_surprise() else EMPTY_STRING,
    'sunny': SUN_EMOJI,
    'tstorms': RAIN_AND_STORM_EMOJI,
    'unknown': QUESTION_EMOJI + QUESTION_EMOJI + QUESTION_EMOJI,
}

MOON_MAP = {
    'new moon': NEW_MOON_EMOJI,
    'new': NEW_MOON_EMOJI,
    'waxing crescent': WAXING_CRESCENT_MOON_EMOJI,
    'first quarter': FIRST_QUARTER_MOON_EMOJI,
    'waxing gibbous': WAXING_GIBBOUS_MOON_EMOJI,
    'full moon': FULL_MOON_EMOJI,
    'full': FULL_MOON_EMOJI,
    'waning gibbous': WANING_GIBBOUS_MOON_EMOJI,
    'last quarter': LAST_QUARTER_MOON_EMOJI,
    'waning crescent': WANING_CRESCENT_MOON_EMOJI
}


def current_hour_and_minute():
    now = datetime.datetime.now()
    return now.hour


def get_state(sunrise, sunset, current):

    sunrise_hour = int(sunrise['hour'])
    sunset_hour = int(sunset['hour'])

    if sunrise_hour == current:
        return STATE_SUNRISE
    elif sunset_hour == current:
        return STATE_SUNSET
    elif sunrise_hour < current < sunset_hour:
        return STATE_DAY
    else:
        return STATE_NIGHT


def emoji_for(icon, state, moon_phase):
    emoji = WEATHER_ICON_TO_EMOJI_MAP[icon]

    if emoji == 'clear':
        if state == STATE_DAY:
            emoji = SUN_EMOJI
        elif state == STATE_NIGHT:
            emoji = MOON_MAP[moon_phase]

    if state == STATE_SUNRISE:
        emoji += SUNRISE_MOUNTAINS_EMOJI if random.random() < 0.5 else SUNRISE_EMOJI
    elif state == STATE_SUNSET:
        emoji += SUNSET_EMOJI
    elif state == STATE_NIGHT:
        if is_surprise():
            emoji += NIGHT_WITH_STARTS_EMOJI


    return emoji


def download_json(url):
    f = urllib.request.urlopen(url)
    json_string = f.read().decode('utf-8')
    parsed_json = json.loads(json_string)
    f.close()
    return parsed_json


def create_tweet():
    parsed_json = download_json('http://api.wunderground.com/api/%s/hourly/q/UA/Kyiv.json' % WEATHER_KEY)

    hourly_forecast = parsed_json['hourly_forecast']

    first_hour_forecast = hourly_forecast[0]

    temp = first_hour_forecast['temp']['metric']
    feels_like = first_hour_forecast['feelslike']['metric']
    humidity = first_hour_forecast['humidity']
    icon = first_hour_forecast['icon']

    parsed_json = download_json('http://api.wunderground.com/api/%s/astronomy/q/UA/Kyiv.json' % WEATHER_KEY)

    moon_phase = parsed_json['moon_phase']['phaseofMoon'].lower()

    sun_phase = parsed_json['sun_phase']

    sunset = sun_phase['sunset']
    sunrise = sun_phase['sunrise']
    current_time = current_hour_and_minute()

    state = get_state(sunrise, sunset, current_time)

    emoji = emoji_for(icon, state, moon_phase)

    final_tweet = "%s: %s°C, %s: %s%%, %s %s°C, %s" % \
                  (THERMOMETER_EMOJI, temp, DROPLET_EMOJI, humidity, "feels like", feels_like, emoji)

    print(final_tweet)

    return final_tweet


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
    tweet(create_tweet())
