from twython import TwythonStreamer
import tweepy

CONSUMER_KEY = "06byIs5mugziPmCF7JvNtV8kf"
CONSUMER_SECRET = "UIPdgpcK75MI4TsBDpm1RW7PXG2soBlAmjByHgSD9zborKwg9m"
ACCESS_TOKEN = "2344462854-jDIOnx1heeRqGKjAo9h1ju9UdaCv5gSwZUDPwh9"
ACCESS_SECRET = "JE39Am0k2s9q5pYWIa0Aqv0SmhlICP3cubh89gpdFbDae"

tweets = []

def saveTweet(tweet, movie):
    tweet_data = {}
    tweet_data['movie'] = movie
    tweet_data['tweet'] = tweet
    
class Streamer(TwythonStreamer):
    
    def on_success(self, data):
        if 'text' in data:
            print(data['text'])
                
    def on_fail(self, status_code, data):
        print(data, status_code)
        self.disconnect()
stream = Streamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print("status "+status.text)
    
    def on_data(self, data):
        print("data "+data)
        return True

    def on_error(self, status):
        print("error "+ str(status))
        
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
        
movieFilePath  = "MovieList.txt"
movieFile = open(movieFilePath, encoding="utf8")
myStream.filter(track=['python'], is_async=True)

i = 1
for movie in movieFile:
    movie = movie.strip()
    print("Getting tweets for movie " + str(i))
    i += 1
    #stream.statuses.filter(track=movie)
    myStream.filter(track=['python'], is_async=True)