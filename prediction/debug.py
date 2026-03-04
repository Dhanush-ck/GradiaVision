import joblib
import pandas as pd

model = joblib.load("random_forest.pkl")

# Load dataset again
df = pd.read_csv("./dataset/dataset.csv")

print("\nDataset Statistics:\n")
print(df.describe())

print("\nFeature Importance:\n")
importance_df = pd.DataFrame({
    "feature": df.drop("next_sgpa", axis=1).columns,
    "importance": model.feature_importances_
}).sort_values(by="importance", ascending=False)

print(importance_df)
