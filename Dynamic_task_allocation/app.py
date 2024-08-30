from flask import Flask, request, jsonify
import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

classifier = joblib.load('issue_classifier_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
app = Flask(__name__)

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    return ' '.join(lemmatized_tokens)

@app.route('/classify', methods=['POST'])
def classify_issue():
    data = request.get_json(force=True)
    issue_text = data.get('text', '')
    
    processed_issue = preprocess_text(issue_text)
    features = tfidf_vectorizer.transform([processed_issue])
    classification = classifier.predict(features)[0]
    
    # Return the response as JSON
    response = {
        'text': issue_text,
        'classification': classification
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
