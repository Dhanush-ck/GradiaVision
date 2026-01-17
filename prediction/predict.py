import joblib
import pandas as pd

model = joblib.load("random_forest.pkl")

def predict_score(prev_sgpa, avg_sgpa, sgpa_trend, avg_marks, avg_difficulty, avg_study_hours, planned_effort):
    feature_names = [
        "prev_sgpa",
        "avg_sgpa",
        "sgpa_trend",
        "avg_marks",
        "avg_difficulty",
        "avg_study_hours",
        "planned_effort"
    ]

    features_df = pd.DataFrame([[
    prev_sgpa,
    avg_sgpa,
    sgpa_trend,
    avg_marks,
    avg_difficulty,
    avg_study_hours,
    planned_effort,
    ]], columns=feature_names)

    predicted_sgpa = model.predict(features_df)[0]
    print("Predicted SGPA:", round(predicted_sgpa, 2))
    

# predict_score(5.70, 5.60, -10.0, 48.0, 4.3, 1.4, 1.0)
# predict_score(6.20, 6.10, -0.05, 55.0, 3.8, 2.2, 2.0)