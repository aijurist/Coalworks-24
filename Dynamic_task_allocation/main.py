import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import apply_features
from dummy_data import shift_log_data, workers_data, training_data
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

def extract_features(text):
    tokens = word_tokenize(text.lower())
    features = {word: (word in tokens) for word in words}
    return features

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text


sentiment_analyzer = SentimentIntensityAnalyzer()
def get_sentiment(text):
    scores = sentiment_analyzer.polarity_scores(text)
    sentiment = scores['pos']
    return sentiment

words = set(word for sentence, _ in training_data for word in word_tokenize(sentence.lower()))
training_features = [(extract_features(text), label) for text, label in training_data]
classifier = NaiveBayesClassifier.train(training_features)

def identify_issue(issue):
    features = extract_features(issue)
    return classifier.classify(features)
    
# new_issues = [data[7] for worker_id, data in shift_log_data.items()]
new_issues = ['My JCB is giving more sound.', 'Water is leaking from the roof of my JCB', 'Brake is loose in my truck', 'My truck tyre is flat', "I need to go to urine, dehydrating", "I killed my coworker, I will also kill you, fouck you!", "Suoervisor is late by 12hours", "Roofholder spring does work"]

# Classify each new issue
for issue in new_issues:
    classification = identify_issue(issue)
    sentiment = get_sentiment(issue)
    print(f"Issue: '{issue}' classified as: {classification}. Sentiment Analysis: {sentiment}")
