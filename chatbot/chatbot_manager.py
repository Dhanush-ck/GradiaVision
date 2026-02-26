import os
from django.conf import settings
import joblib
import random
import re

INTENT_MODEL_PATH = os.path.join(settings.BASE_DIR, 'chatbot', 'intent_model.pkl')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'chatbot', 'vectorizer.pkl')

model = joblib.load(INTENT_MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def generate_reply(msg):

    if msg.lower() == '/sgpa':
        return 'sgpa'
    
    if msg.lower().startswith("/change"):
        parts = msg.lower().split()

        if len(parts) != 4:
            return 'change'

        toughness = float(parts[1])
        study_hours = float(parts[2])
        planned_effort = float(parts[3])

        return {
            'type': 'change', 
            'values': [toughness, study_hours, planned_effort],
            }

    vec = vectorizer.transform([msg])
    intent = model.predict(vec)[0]

    probs = model.predict_proba(vec)
    confidence = max(probs[0])

    if confidence < 0.5:
        # print(intent, confidence)
        intent = "fallback"

    # print(intent)
    if intent == "greeting":
        replies = [
            "Hello! How can I help you? 😊",
            "Hi there! What can I do for you?",
            "Hey! Need any help?",
            "Welcome! Ask me anything.",
            "Hi! I'm here to help 🚀"
        ]

        return random.choice(replies)

    elif intent == "study_tips":
        replies = [
            "Try studying in short focused sessions (25–30 mins) with small breaks. Consistency beats cramming 📚",
            "Make a daily study plan and revise before sleeping — your brain remembers better overnight 😴",
            "Practice questions after learning a topic. Active recall improves memory a lot!",
            "Don’t just read — write summaries or teach the topic to yourself 👨‍🏫",
            "Start with difficult subjects when your energy is high, save easier ones for later.",
            "Revise regularly and track your weak areas. Improvement comes from fixing mistakes 💪",
            "Study smart: understand concepts first, then memorize.",
            "Keep distractions away and reward yourself after completing tasks 🎯"
        ]

        return random.choice(replies)

    elif intent == "attendance_issue":
        replies = [
            "You need minimum 75% attendance to write exams without condonation. Let’s fix this 💪",
            "Attendance alert 🚨 Try to reach 75% to avoid academic trouble.",
            "Regular classes = better scores + exam eligibility. Target 75%!",
            "Missing classes hurts both attendance and understanding. Aim for 75%+.",
            "You’re close — attend upcoming classes and push your attendance above 75%."
        ]

        return random.choice(replies)

    elif intent == "stress_motivation":
        replies = [
            "Take a deep breath — you’re doing better than you think 💙 One step at a time.",
            "It’s okay to feel stressed. Pause, reset, and keep moving forward 💪",
            "Remember: tough times don’t last, strong students do 🌱",
            "You don’t have to be perfect — just keep progressing.",
            "Small efforts every day lead to big results. You’ve got this 🚀",
            "Stress means you care — now channel that energy into action.",
            "Close your eyes, breathe slowly, and start again. I believe in you 😊",
            "Your future self will thank you for not giving up today."
        ]

        return random.choice(replies)

    elif intent == "target_percentage":

        percentage = re.search(r'\b(100|[1-9]?\d)\s*(%|percent|percentage)?\b', msg.lower())
        if 'sgpa' in msg.lower() or percentage <= 10:
            percentage *= 10
        if percentage:
            target_percentage = int(percentage.group(1))

        # return f"You need this {target_percentage} to achieve the target"
        return {
            'type': 'percentage',
            'percentage': target_percentage
            }

    elif intent == "goodbye":
        replies = [
            "Goodbye! Take care 👋",
            "See you later! All the best 🚀",
            "Bye! Feel free to come back anytime 😊",
            "Catch you soon — keep learning!",
            "Good luck with your work! 👋"
        ]

        return random.choice(replies)

    elif intent == "fallback":
        return "Sorry, can you rephrase?"

    else:
        return "Cannot identify"