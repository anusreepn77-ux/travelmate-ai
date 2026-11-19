import os
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

def train_recommender():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'destinations_dataset.csv')
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} destinations for training.")

    # Feature string combining category, climate, district, highlights
    df['combined_features'] = df['category'] + ' ' + df['climate'] + ' ' + df['district'] + ' ' + df['highlights']

    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])

    # Normalize numerical features (budget, popularity, rating)
    scaler = MinMaxScaler()
    num_features = scaler.fit_transform(df[['average_budget', 'popularity_score', 'rating']])

    # Combined dense representation for KNN
    combined_features = np.hstack([tfidf_matrix.toarray(), num_features])

    # Fit Nearest Neighbors Model
    knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn.fit(combined_features)

    # Save models
    saved_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
    os.makedirs(saved_dir, exist_ok=True)

    joblib.dump(knn, os.path.join(saved_dir, 'recommender_knn.joblib'))
    joblib.dump(tfidf, os.path.join(saved_dir, 'tfidf_vectorizer.joblib'))
    joblib.dump(scaler, os.path.join(saved_dir, 'recommender_scaler.joblib'))
    joblib.dump(df, os.path.join(saved_dir, 'destinations_df.joblib'))

    print("KNN Recommender model & TF-IDF vectorizer saved successfully!")

    # Quick test inference
    sample_text = "Hill Station Cool Tea gardens trekking"
    vec = tfidf.transform([sample_text]).toarray()
    sample_num = scaler.transform([[8000, 90, 4.8]])
    sample_feat = np.hstack([vec, sample_num])
    distances, indices = knn.kneighbors(sample_feat, n_neighbors=3)

    print("\n--- Model Evaluation (KNN Top-3 Query Test) ---")
    for idx, dist in zip(indices[0], distances[0]):
        print(f"Match: {df.iloc[idx]['name']} ({df.iloc[idx]['district']}) - Distance: {dist:.4f}")

if __name__ == '__main__':
    train_recommender()
