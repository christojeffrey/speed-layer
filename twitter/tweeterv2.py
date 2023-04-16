# twitter stream listener using tweepy
import tweepy
import time
import os
from dotenv import load_dotenv


load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
# get from .env file one level up

class StreamListener(tweepy.Stream):
    def on_status(self, status):
        print(status.text)
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

# do streaming with keyword  "python"
stream_listener = StreamListener(
    TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

stream_listener.filter(track=["python"])

