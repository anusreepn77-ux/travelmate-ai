import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, r2_score

def train_best_time():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'weather_dataset.csv')
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} weather records.")

    features = ['destination', 'month', 'avg_temp', 'rainfall_mm', 'humidity', 'crowd_level']
    X = df[features]
    y_class = df['season_label']
    y_reg = df['visit_score']

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['destination']),
            ('num', 'passthrough', ['month', 'avg_temp', 'rainfall_mm', 'humidity', 'crowd_level'])
        ]
    )

    X_train, X_test, y_train_c, y_test_c, y_train_r, y_test_r = train_test_split(
        X, y_class, y_reg, test_size=0.2, random_state=42, stratify=y_class
    )

    # 1. Random Forest Classifier
    rf_clf = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    rf_clf.fit(X_train, y_train_c)
    pred_c = rf_clf.predict(X_test)
    acc = accuracy_score(y_test_c, pred_c)
    print(f"\n[Random Forest Classifier] Accuracy: {acc:.4f}")
    print(classification_report(y_test_c, pred_c))

    # 2. Decision Tree Classifier
    dt_clf = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', DecisionTreeClassifier(max_depth=6, random_state=42))
    ])
    dt_clf.fit(X_train, y_train_c)
    dt_pred = dt_clf.predict(X_test)
    dt_acc = accuracy_score(y_test_c, dt_pred)
    print(f"[Decision Tree Classifier] Accuracy: {dt_acc:.4f}")

    # 3. Random Forest Regressor for visit_score (1-100)
    rf_reg = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    rf_reg.fit(X_train, y_train_r)
    pred_r = rf_reg.predict(X_test)
    mae = mean_absolute_error(y_test_r, pred_r)
    r2 = r2_score(y_test_r, pred_r)
    print(f"[Random Forest Visit Score Regressor] MAE: {mae:.2f}, R2: {r2:.4f}")

    # Save models
    saved_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
    os.makedirs(saved_dir, exist_ok=True)

    joblib.dump(rf_clf, os.path.join(saved_dir, 'best_time_rf.joblib'))
    joblib.dump(dt_clf, os.path.join(saved_dir, 'best_time_dt.joblib'))
    joblib.dump(rf_reg, os.path.join(saved_dir, 'best_time_score_reg.joblib'))

    print("Weather & Best Time Predictor models saved successfully!")

if __name__ == '__main__':
    train_best_time()
