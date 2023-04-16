# twitter stream listener using tweepy
import tweepy
import time
import os
from dotenv import load_dotenv


load_dotenv()

# get from .env file one level up
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")



class MyStreamListener(tweepy.StreamingClient):
    def ob_connect(self):
        print("You are connected to the Twitter API")

    def on_tweet(self, tweet):
        # discard tweets that are retweets
        if tweet.referenced_tweets == None:
            print(tweet.text)
        # add delay to avoid rate limit 10K tweets per month
        print("delaying for ", 10000/60/60/24/30, " seconds")
        time.sleep(10000/60/60/24/30)


client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=TWITTER_API_KEY, consumer_secret=TWITTER_API_KEY_SECRET,access_token=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)


# user look up
user = client.get_user(username="twitterdev")
print(user)
# do streaming with keyword  "python"
# stream.add_rules(tweepy.StreamRule("python"))
# stream.filter(tweet_fields=["referenced_tweets", "text"], languages=["en"])

