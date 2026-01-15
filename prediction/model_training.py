import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib


df  = pd.read_csv('./dataset/dataset.csv')

x = df.drop("next_sgpa", axis=1)
y = df["next_sgpa"]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(x_train, y_train)

predictions = model.predict(x_test)

print("MAE: ", mean_absolute_error(y_test, predictions))
print("R2 Score: ", r2_score(y_test, predictions))

joblib.dump(model, "random_forest.pkl")

print("Model Created")