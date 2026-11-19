import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_cost_predictor():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'cost_dataset.csv')
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} travel cost profiles.")

    features = ['destination', 'days', 'travelers', 'accommodation_type', 'transport_type']
    X = df[features]
    y = df['total_cost']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['destination', 'accommodation_type', 'transport_type']),
            ('num', 'passthrough', ['days', 'travelers'])
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=120, random_state=42))
    ])

    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    print(f"\n[AI Travel Cost Regressor]")
    print(f"Mean Absolute Error (MAE): ₹{mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): ₹{rmse:.2f}")
    print(f"R² Score: {r2:.4f}")

    saved_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
    os.makedirs(saved_dir, exist_ok=True)
    joblib.dump(model, os.path.join(saved_dir, 'cost_predictor.joblib'))
    print("Cost Predictor ML model saved successfully!")

    # Test sample inference
    sample_df = pd.DataFrame([{
        'destination': 'Munnar',
        'days': 4,
        'travelers': 2,
        'accommodation_type': 'Standard Hotel',
        'transport_type': 'Private Sedan'
    }])
    pred_cost = model.predict(sample_df)[0]
    print(f"\nSample Prediction for Munnar, 4 days, 2 travelers (Standard Hotel + Private Sedan): ₹{pred_cost:.2f}")

if __name__ == '__main__':
    train_cost_predictor()
