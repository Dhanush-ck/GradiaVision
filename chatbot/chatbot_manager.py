import os
from django.conf import settings
import joblib

INTENT_MODEL_PATH = os.path.join(settings.BASE_DIR, 'chatbot', 'intent_model.pkl')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'chatbot', 'vectorizer.pkl')

model = joblib.load(INTENT_MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def generate_reply(msg):

    vec = vectorizer.transform([msg])
    intent = model.predict(vec)[0]

    probs = model.predict_proba(vec)
    confidence = max(probs[0])

    if confidence < 0.5:
        # print(intent, confidence)
        intent = "fallback"

    # print(intent)
    if intent == "greeting":
        return "Hello, how can i help you!!"

    elif intent == "predict":
        return 'predict'

    elif intent == "study_tips":
        return "Try studying 2–3 hours daily."

    elif intent == "attendance_issue":
        return "Maintain at least 75% attendance."

    elif intent == "stress_motivation":
        return "stress"

    elif intent == "target_percentage":
        return "target percentage"

    elif intent == "goodbye":
        return "Bye see ya again"

    elif intent == "fallback":
        return "Sorry, can you rephrase?"

    else:
        return "Cannot identify"