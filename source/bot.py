import tweepy
from secrets import *
from simpleURL import *
from wikiScraper import *


# create OAuthHandler instance

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_secret)

# create API instance

api = tweepy.API(auth)


# create a class inheriting from the the tweepy StreamListener

class BotStream(tweepy.StreamListener):

    def on_status(self, status):

        username = status.user.screen_name

        status_id = status.id

        mentions = api.mentions_timeline(count = 1)

        tweetText = mentions[0].text

        print(tweetText)

        #wikiHTML = simple_get(hasLink(tweetText))

        try:
            path = distance(hasLink(tweetText))
            api.update_status('It will take '
                          + str(len(path))
                          + ' clicks to get to the US from '
                          + hasLink(tweetText) + ' @' + username,
                          in_reply_to_status_id = status_id)
        except:
             api.update_status('Please provide a Wikipedia article!', in_reply_to_status_id = status_id)
        

        


    

myStreamListener = BotStream()

#Construct Stream instance

stream = tweepy.Stream(auth, myStreamListener)

stream.filter(track=['@clicks2usa'])
