from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
from etl import save
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# VADER sentiment analyzer
nltk.download('vader_lexicon')

# generate labels to use for classification using sentiment analysis
def generate_labels(comments, threshold=0.05):
    sia = SentimentIntensityAnalyzer()
    labels = []
    # loop through comments and analyze
    for comment in comments:
        sentiment = sia.polarity_scores(comment)
        # agree
        if sentiment['compound'] > threshold:
            labels.append(2)
        # disagree
        elif sentiment['compound'] < threshold*-1:
            labels.append(0)
        # neutral
        else:
            labels.append(1)
    return labels

# classification model using scikit-learn to be used on comments
class CommentClassifier:
    def __init__(self, max_features=5000):
        # TF-IDF vectorizer: converts text data into numerical features based on term frequency and inverse document frequency
        self.vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english')
        # XGBoost classifier: decision tree ML library for regression & classification
        self.model = xgb.XGBClassifier(eval_metric='logloss')

    # trains the classifier
    def fit(self, comments, labels):
        # convert comments into numerical features
        X = self.vectorizer.fit_transform(comments)
        # split the dataset into training and testing subsets
        # 80% train, 20% test
        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)
        # train the model on the training data
        self.model.fit(X_train, y_train)
        # save the test data
        self.X_test = X_test
        self.y_test = y_test
        return self

    # predicts labels using the trained model
    def predict(self, comments):
        # convert comments into numerical features
        X = self.vectorizer.transform(comments)
        # predict labels
        return self.model.predict(X)

    # assesses model performance
    def evaluate(self):
        # use the model to predict labels on the test dataset
        y_pred = self.model.predict(self.X_test)
        # assess and save results
        report = classification_report(self.y_test, y_pred, zero_division=0)
        cm = confusion_matrix(self.y_test, y_pred)
        # assess performance and print results
        save.print_classification_report(report, cm)
        return self.y_test, y_pred
