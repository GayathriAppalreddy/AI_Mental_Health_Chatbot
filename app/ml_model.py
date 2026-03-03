import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = 'models/sentiment_model.pkl'
VECT_PATH = 'models/vectorizer.pkl'


def train():
    """Train or retrain the sentiment model using data/training_data.csv.
    If the csv is missing or empty the script falls back to a small hard-coded dataset.
    """
    # load training data from csv if available
    df = None
    if os.path.exists('data/training_data.csv'):
        try:
            df = pd.read_csv('data/training_data.csv')
            # ensure sentiment encoded as numeric
            if df['sentiment'].dtype == object:
                df['sentiment'] = df['sentiment'].map({'Positive': 1, 'Negative': 0})
        except Exception as e:
            print("error reading training_data.csv", e)
            df = None

    if df is None or df.empty:
        # fallback to small built-in dataset
        data = {
            'text': [
                'I feel very happy and great', 'Today is a wonderful day',
                'I am so depressed and sad', 'I feel lonely and anxious',
                'I am doing okay', 'Everything is fine'
            ],
            'sentiment': [1, 1, 0, 0, 1, 1]
        }
        df = pd.DataFrame(data)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['text'])
    y = df['sentiment']

    model = LogisticRegression()
    model.fit(X, y)

    # make sure models directory exists
    os.makedirs('models', exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    with open(VECT_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)

    print("Model trained and saved to", MODEL_PATH)
    return model, vectorizer


def predict_mood(user_text):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECT_PATH):
        train()
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECT_PATH, 'rb') as f:
        vectorizer = pickle.load(f)

    vec_text = vectorizer.transform([user_text])
    prediction = model.predict(vec_text)

    return "Positive" if prediction[0] == 1 else "Negative"


if __name__ == '__main__':
    train()
