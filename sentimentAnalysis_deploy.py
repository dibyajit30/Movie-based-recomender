# Importing the libraries
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('sentiment140-mini.csv',names=["label", "ID", "Date", "Query","user","tweet"], encoding='latin-1')
dataset_movieTweets = pd.read_csv('tweetsDataset.csv',names=["screen_name", "name", "location", "time","movie_name","tweet"], encoding='latin-1')

# Cleaning the texts
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Preprocessing
corpus = []
atPattern = "@[\w]*"
urlPattern = "https?://[A-Za-z0-9./]+"
length = len(dataset)
for i in range(length):
    print("Preprocessing training data:" + str((i*100)/length) + "%")
    tweet = dataset['tweet'][i]
    atTheRates = re.findall(atPattern, tweet)
    for atTheRate in atTheRates:
        tweet = re.sub(atTheRate,"",tweet)
    tweet = re.sub(urlPattern,"",tweet)    
    tweet = re.sub('[^a-zA-Z]', ' ', tweet)
    tweet = tweet.lower()
    tweet = tweet.split()
    ps = PorterStemmer()
    tweet = [ps.stem(word) for word in tweet if not word in set(stopwords.words('english'))]
    tweet = ' '.join(tweet)
    corpus.append(tweet)

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_df=0.80, min_df=2, max_features = 5000)
X_train = cv.fit_transform(corpus).toarray()
y_train = dataset.iloc[:, 0].values

# Fitting Decision Tree to the Training set
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# Actual data preprocessing and prediction
corpus = []
length = len(dataset_movieTweets)
for i in range(length):
    print("Preprocessing actual data:" + str((i*100)/length) + "%")
    tweet = dataset_movieTweets['tweet'][i]
    atTheRates = re.findall(atPattern, tweet)
    for atTheRate in atTheRates:
        tweet = re.sub(atTheRate,"",tweet)
    tweet = re.sub(urlPattern,"",tweet)    
    tweet = re.sub('[^a-zA-Z]', ' ', tweet)
    tweet = tweet.lower()
    tweet = tweet.split()
    ps = PorterStemmer()
    tweet = [ps.stem(word) for word in tweet if not word in set(stopwords.words('english'))]
    tweet = ' '.join(tweet)
    corpus.append(tweet)

X_test = cv.transform(corpus).toarray()
y_pred = classifier.predict(X_test)

# Saving the predictions
output = []
for i in range(length):
    if y_pred[i] > 0:
        output.append(dataset_movieTweets.iloc[i])
outputFile = "positiveTweetsDataset.csv"
tweetFile = open(outputFile, encoding="utf8")
save = pd.DataFrame(output)
save.to_csv(outputFile, index = False)
save.tail()