from decouple import config # Used to read from .env file
from twitch_info import get_user_id, get_stream, get_access_token # Used to get stream info from Twitch API
import tweepy # Used to post on Twitter
import logging # Used to log messages
import json # Used to read from json file 
import emoji # Used to handle emojis

def goodbye(team_name):
    """
    This functio nis used to save all current data such as who is online in order to not tweet the same message twice. 
    It also logs the fact that the program shut down.
    """
    fw = open('users.json', 'w')
    json.dump(team_name, fw)
    fw.close()
    logging.info('Goodbye!')
    print('Goodbye!')

import atexit # Used to register a function to be run at program exit



# Logging
logging.basicConfig(filename="log.txt", level=logging.INFO, format='%(asctime)s %(message)s')

# Twitter API Credentials
consumer_key = config('TWITTER_API_KEY', default='')
consumer_secret = config('TWITTER_SECRECT_KEY', default='')
access_token = config('TWITTER_ACCESS_TOKEN', default='')
access_token_secret = config('TWITTER_ACCESS_TOKEN_SECRET', default='')

# Twitch API Credentials
client_id = config('TWITCH_CLIENT_ID', default='')
client_secret = config('TWITCH_CLIENT_SECRET', default='')
acces_token = get_access_token(client_id=client_id, client_secret=client_secret)

# Twitter API Setup
client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)

# Twitch usernames to monitor
f = open('users.json', 'r')
team = json.load(f)

atexit.register(goodbye, team)

print("Running...")

# Main Loop
while True:
    #Connect the Twitch API
    for(username) in team:
        """
        Here we are looking if the streamer is online and if he is, we are getting the streamer's info such as the title etc.
        Later on we will use this info to tweet on the account. We will also modify the array in order to not tweet the same message twice.
        """
        user_id = get_user_id(user_name=username, client_id=client_id, acces_token=acces_token)
        stream = get_stream(user_id=user_id, client_id=client_id, acces_token=acces_token)
        try:
            if stream['title']:
                if team[username]["isLive"] == 0:
                    team[username]["isLive"] = 1
                    demojized = emoji.demojize(stream['title'])
                    title = demojized.split('//')[0] # Here we used demojize because the split function would throw an error if we kept the raw output because of emojis.
                    emojized = emoji.emojize(title) # We remojized the string again here.
                    caps = username.upper()
                    game = stream["game_name"].upper()
                    message = "{} LIVE {} {} \n twitch.tv/{}".format(caps, game, emojized, username)
                    response = client.create_tweet(text=message)
                    id = response.data["id"]
                    logging.info("Created Tweet: https://twitter.com/FariStream/status/{}".format(id)) # Here we log the tweet 
        except TypeError:
            if team[username]["isLive"] == 1:
                team[username]["isLive"] = 0
                logging.info("{} is offline".format(username))
        except tweepy.errors.Forbidden:
            logging.error("Tweeting again")
        except Exception as e:
            logging.error("Something went wrong: {}".format(e))
