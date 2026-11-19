import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_sentiment():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'reviews_dataset.csv')
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} tourist reviews for sentiment analysis.")

    X = df['review_text']
    y = df['sentiment']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # TF-IDF + Logistic Regression Pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=1500, stop_words='english')),
        ('classifier', LogisticRegression(C=1.0, max_iter=200, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    # Evaluation
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n[Tourist Review Sentiment Classifier] Accuracy: {acc:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Save trained pipeline
    saved_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
    os.makedirs(saved_dir, exist_ok=True)
    joblib.dump(pipeline, os.path.join(saved_dir, 'sentiment_pipeline.joblib'))
    print("Sentiment Analysis ML pipeline saved successfully!")

    # Test sample inference
    test_texts = [
        "Unbelievable beauty, fresh air, clean homestay and great food!",
        "Dirty room, rude staff and worst experience ever.",
        "Average trip, nothing special but okay for a short weekend."
    ]
    print("\n--- Live Test Inferences ---")
    for t in test_texts:
        pred = pipeline.predict([t])[0]
        probs = pipeline.predict_proba([t])[0]
        max_prob = max(probs)
        print(f"'{t[:40]}...' -> {pred} ({max_prob*100:.1f}%)")

if __name__ == '__main__':
    train_sentiment()
