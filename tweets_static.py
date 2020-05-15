from twython import Twython
import time
import pandas as pd

CONSUMER_KEY = "06byIs5mugziPmCF7JvNtV8kf"
CONSUMER_SECRET = "UIPdgpcK75MI4TsBDpm1RW7PXG2soBlAmjByHgSD9zborKwg9m"

python_tweets = Twython(CONSUMER_KEY, CONSUMER_SECRET)
dict_ = {'movie': [], 'user': [], 'date': [], 'text': [], 'id': []}

inputMovieFile  = "MovieList.txt"
movieFile = open(inputMovieFile, encoding="utf8")
outputFile = "tweetsDataset.csv"
tweetFile = open(outputFile, 'a', encoding="utf8")
movieList = []
for movie in movieFile:
    movieList.append(movie.strip())
    
movieLength = len(movieList)
tweet_per_movie = 10

lowerIndex = 0
upperIndex = movieLength
sleep_time = 900
while lowerIndex < upperIndex:
    for i in range(lowerIndex, lowerIndex+450):
        print("Fetching tweets for movie:" + str(i))
        query = {
            'q' : movieList[i],
            'count': tweet_per_movie,
            'lang': 'en'
        }
        for tweet in python_tweets.search(**query)['statuses']:
            row = {'screen_name': tweet['user']['screen_name'], 'name': tweet['user']['name'],
                   'location': tweet['user']['location'], 'time': tweet['created_at'],
                   'movie_name': movieList[i], 'tweet': tweet['text']}
            save = pd.DataFrame(row, index=[0])
            save.to_csv(tweetFile, header=False, index=False)
    print("Waiting...")
    time.sleep(900)
    lowerIndex += 450
        
save.tail()