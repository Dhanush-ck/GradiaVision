import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# 1. Load the BALANCED dataset
data = pd.read_csv("./dataset/balanced_intent_dataset.csv") 

X = data["text"]
y = data["intent"]

# 2. Add Train-Test Split (CRITICAL STEP)
# This lets you see how the model performs on data it HASN'T seen yet.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Enhanced Vectorizer
# Adding 'ngram_range=(1,2)' helps the model understand phrases like "not happy" 
# instead of just "not" and "happy" separately.
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 4. Logistic Regression
# Since your data is now balanced, you don't strictly NEED class_weight='balanced',
# but keeping it doesn't hurt.
model = LogisticRegression(max_iter=1000) 
model.fit(X_train_vec, y_train)

# 5. Evaluate - This shows you the TRUE performance
y_pred = model.predict(X_test_vec)
print("--- Model Evaluation ---")
print(classification_report(y_test, y_pred))

# 6. Save the model and the vectorizer
joblib.dump(model, "intent_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("\nModel and Vectorizer saved successfully!")