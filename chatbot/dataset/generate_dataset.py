import pandas as pd
import random

TOTAL_PER_INTENT = 200

greeting_base = [
    "hi", "hello", "hey mentor", "good morning", "good evening",
    "hello mentor", "hi sir", "hey", "morning mentor"
]

study_base = [
    "how to improve marks",
    "marks are low",
    "not scoring well",
    "how to study better",
    "give me study tips",
    "how to prepare for exams",
    "how to improve performance",
    "suggest study plan",
    "need guidance for studies"
]

attendance_base = [
    "low attendance problem",
    "attendance issue",
    "my attendance is low",
    "how to improve attendance",
    "attendance shortage",
    "risk due to attendance"
]

stress_base = [
    "i am stressed",
    "exam stress",
    "feeling anxious",
    "academic pressure",
    "lack of motivation",
    "feeling demotivated",
    "how to stay motivated"
]

percentage_templates = [
    "how can i get {}%",
    "i want {} percent",
    "tips to score {}%",
    "how to reach {}%",
    "aiming for {}%",
    "need {}% in exams",
    "target is {} percent",
    "how to secure {}%"
]

casual_words = ["", " mentor", " bro", " please", " sir"]

rows = []

def generate_sentences(base_list, intent):
    data = []
    while len(data) < TOTAL_PER_INTENT:
        base = random.choice(base_list)
        casual = random.choice(casual_words)
        sentence = base + casual
        data.append([sentence.lower(), intent])
    return data


# Greetings
rows += generate_sentences(greeting_base, "greeting")

# Study Tips
rows += generate_sentences(study_base, "study_tips")

# Attendance
rows += generate_sentences(attendance_base, "attendance_issue")

# Stress
rows += generate_sentences(stress_base, "stress_motivation")

# Target Percentage
percent_rows = []
while len(percent_rows) < TOTAL_PER_INTENT:
    p = random.choice(range(50, 96, 5))
    temp = random.choice(percentage_templates)
    casual = random.choice(casual_words)
    sentence = temp.format(p) + casual
    percent_rows.append([sentence.lower(), "target_percentage"])

rows += percent_rows

random.shuffle(rows)

df = pd.DataFrame(rows, columns=["text", "intent"])
df.to_csv("intent_dataset.csv", index=False)

print("Dataset generated successfully!")
print("Total rows:", len(df))
