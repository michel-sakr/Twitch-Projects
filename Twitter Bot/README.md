# Requirements:

Sign up for Twitter Developer
Sign up for Twitch Developer

Initialize apps and get keys from Twitch and Twitter.

# Idea:

Send a request using Twitch's API in order to retreive information about the streamer we are looking up.
If he is live, we Tweet using the Twitter API about him, where we add details such as the game he is playing, the title and the link.
Finally, everything is logged in log.txt in order to keep track of all tweets, as well as when the program is exited.
There are multiple streamers with their usernames stored in a JSON file. We loop through each one and tweet on one same account.

# Room for development:

We could, in addition to tweeting from the main account, add a feature to retweet from the personal account of each user. We would then have two interactions with the Twitter servers but from 2 different accounts.

# Libraries used:

tweepy => To use the Twitter API \n
twitch-info => To use the Twitch API \n
decouple => To extract info from the .env file \n
emoji => To turn emojis into strings and vice versa in order to manipulate titles without encountering exceptions \n
logging => To log all data \n
json => To read from JSON \n
atexit => To execute function when exiting program \n
