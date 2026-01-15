import random
import pandas as pd

def generate_realistic_dataset(n_samples=500):
    rows = []

    for _ in range(n_samples):

        # -------------------------------
        # Base academic performance
        # -------------------------------
        prev_sgpa = round(random.uniform(5.5, 9.5), 2)

        avg_sgpa = round(
            prev_sgpa + random.uniform(-0.25, 0.25), 2
        )

        avg_sgpa = min(max(avg_sgpa, 5.0), 9.8)

        sgpa_trend = round(avg_sgpa - prev_sgpa, 2)

        avg_marks = round(
            (avg_sgpa / 10) * 100 + random.uniform(-5, 5), 2
        )
        avg_marks = min(max(avg_marks, 45), 95)

        # -------------------------------
        # Feedback / effort attributes
        # -------------------------------
        avg_difficulty = round(random.uniform(1.5, 4.5), 2)

        avg_study_hours = round(
            2.0 + (avg_sgpa - 6.0) * 0.6 + random.uniform(-0.5, 0.5), 2
        )
        avg_study_hours = min(max(avg_study_hours, 1.0), 6.0)

        planned_effort = min(
            max(int((avg_study_hours / 6) * 5 + random.uniform(-1, 1)), 1),
            5
        )

        # -------------------------------
        # NEXT SGPA (Target)
        # -------------------------------
        next_sgpa = (
            0.55 * avg_sgpa +
            0.25 * prev_sgpa +
            0.10 * (avg_marks / 10) +
            0.15 * avg_study_hours +
            0.15 * planned_effort -
            0.10 * avg_difficulty +
            random.uniform(-0.15, 0.15)
        )

        # realistic bounds
        next_sgpa = round(min(max(next_sgpa, 5.0), 9.8), 2)

        rows.append({
            "prev_sgpa": prev_sgpa,
            "avg_sgpa": avg_sgpa,
            "sgpa_trend": sgpa_trend,
            "avg_marks": avg_marks,
            "avg_difficulty": avg_difficulty,
            "avg_study_hours": avg_study_hours,
            "planned_effort": planned_effort,
            "next_sgpa": next_sgpa
        })

    return pd.DataFrame(rows)


# Generate dataset
df = generate_realistic_dataset(500)

print(df.describe())

# Save dataset
df.to_csv("dataset.csv", index=False)
