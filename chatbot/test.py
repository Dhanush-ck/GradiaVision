import joblib

model = joblib.load("intent_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

print("Enter the message")
msg = input()

vec = vectorizer.transform([msg])
intent = model.predict(vec)[0]

probs = model.predict_proba(vec)
confidence = max(probs[0])

if confidence < 0.5:
    print(intent, confidence)
    intent = "fallback"

print(intent)
if intent == "greeting":
    print("Hello, how can i help you!!")

elif intent == "predict":
    print('predict')

elif intent == "study_tips":
    print({"reply":"Try studying 2–3 hours daily."})

elif intent == "attendance_issue":
    print({"reply":"Maintain at least 75% attendance."})

elif intent == "stress_motivation":
    print("stress")

elif intent == "target_percentage":
    print("target percentage")

elif intent == "goodbye":
    print("Bye see ya again")

elif intent == "fallback":
    print("Sorry, can you rephrase?")

else:
    print({"Cannot identify"})