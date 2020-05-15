# Importing the libraries
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('sentiment140-mini.csv',names=["label", "ID", "Date", "Query","user","tweet"], encoding='latin-1')

# Cleaning the texts
import re
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Preprocessing
corpus = []
atPattern = "@[\w]*"
urlPattern = "https?://[A-Za-z0-9./]+"
length = len(dataset)
for i in range(length):
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
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 0].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Fitting Neural Network to the Training set
from keras.models import Sequential
from keras.layers import Dense
classifier = Sequential()
classifier.add(Dense(output_dim = 2500, init = 'uniform', activation = 'relu', input_dim = 5000))
classifier.add(Dense(output_dim = 1250, init = 'uniform', activation = 'relu'))
classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
history = classifier.fit(X_train, y_train, batch_size = 100, epochs = 10)

# Predicting the Test set results
y_pred = classifier.predict(X_test)
testSize = len(y_pred)
for i in range(testSize):
    if y_pred[i]>0.5:
        y_pred[i] = 4
    else:
        y_pred[i] = 0

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report
cm = confusion_matrix(y_test, y_pred)
print("Classifier: Neural Network")
print('Confusion Matrix :')
print(cm) 
print('Accuracy Score :',accuracy_score(y_test, y_pred)) 
print('Report : ')
print(classification_report(y_test, y_pred)) 