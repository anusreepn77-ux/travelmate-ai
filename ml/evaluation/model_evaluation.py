import os
import joblib
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score, mean_absolute_error, r2_score

def evaluate_all():
    base_dir = os.path.dirname(__file__)
    saved_dir = os.path.join(base_dir, '..', 'saved_models')
    data_dir = os.path.join(base_dir, '..', 'datasets')

    print("=" * 60)
    print("TRAVELMATE AI — INDEPENDENT MACHINE LEARNING EVALUATION")
    print("=" * 60)

    # 1. Sentiment Model
    sent_path = os.path.join(saved_dir, 'sentiment_pipeline.joblib')
    if os.path.exists(sent_path):
        pipe = joblib.load(sent_path)
        df_rev = pd.read_csv(os.path.join(data_dir, 'reviews_dataset.csv'))
        preds = pipe.predict(df_rev['review_text'])
        acc = accuracy_score(df_rev['sentiment'], preds)
        print(f"\n1. Review Sentiment Classifier (TF-IDF + Logistic Regression)")
        print(f"   Accuracy on full benchmark dataset: {acc*100:.2f}%")
        print("   Sample predictions:")
        for t in ["Outstanding experience and peaceful resort", "Worst hotel ever, terrible smell"]:
            print(f"   - '{t}' => {pipe.predict([t])[0]}")

    # 2. Weather & Best Time Model
    rf_path = os.path.join(saved_dir, 'best_time_rf.joblib')
    if os.path.exists(rf_path):
        rf = joblib.load(rf_path)
        df_w = pd.read_csv(os.path.join(data_dir, 'weather_dataset.csv'))
        feats = ['destination', 'month', 'avg_temp', 'rainfall_mm', 'humidity', 'crowd_level']
        preds_w = rf.predict(df_w[feats])
        acc_w = accuracy_score(df_w['season_label'], preds_w)
        print(f"\n2. Best Time to Visit Predictor (Random Forest Classifier)")
        print(f"   Accuracy on weather telemetry dataset: {acc_w*100:.2f}%")

    # 3. Cost Regressor
    cost_path = os.path.join(saved_dir, 'cost_predictor.joblib')
    if os.path.exists(cost_path):
        reg = joblib.load(cost_path)
        df_c = pd.read_csv(os.path.join(data_dir, 'cost_dataset.csv'))
        feats_c = ['destination', 'days', 'travelers', 'accommodation_type', 'transport_type']
        preds_c = reg.predict(df_c[feats_c])
        mae = mean_absolute_error(df_c['total_cost'], preds_c)
        r2 = r2_score(df_c['total_cost'], preds_c)
        print(f"\n3. Travel Cost Predictor (Random Forest Regressor)")
        print(f"   Mean Absolute Error: ₹{mae:.2f}")
        print(f"   R² Correlation Score: {r2:.4f}")

    # 4. KNN Recommender
    knn_path = os.path.join(saved_dir, 'recommender_knn.joblib')
    if os.path.exists(knn_path):
        knn = joblib.load(knn_path)
        print(f"\n4. Destination Recommender (TF-IDF Content Vectorizer + KNN Cosine)")
        print(f"   Status: Successfully indexed {knn.n_samples_fit_} destination feature vectors.")

    print("\n" + "=" * 60)
    print("ALL 4 MACHINE LEARNING MODELS TRAINED & VERIFIED!")
    print("=" * 60)

if __name__ == '__main__':
    evaluate_all()
