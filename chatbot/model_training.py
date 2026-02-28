import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

from sklearn.metrics import accuracy_score, confusion_matrix
# from sklearn.neighbors import KNeighborsClassifier

data = pd.read_csv("./dataset/balanced_intent_dataset.csv") 

X = data["text"]
y = data["intent"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000) 
# model= KNeighborsClassifier()
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print("--- Model Evaluation ---")
print(classification_report(y_test, y_pred))

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", cm)


joblib.dump(model, "intent_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("\nModel and Vectorizer saved successfully!")

# import seaborn as sns
# import matplotlib.pyplot as plt

# sns.heatmap(cm, annot=True, fmt='d')
# plt.title("Confusion Matrix")
# plt.xlabel("Predicted")
# plt.ylabel("Actual")
# plt.show()