import random
import pandas as pd

def generate_initial_dataset(n_samples):
    rows = []

    for _ in range(n_samples):
        
        # --- Generate base academic performance ---
        prev_sgpa = round(random.uniform(5.5, 9.2), 2)
        avg_sgpa = round(prev_sgpa - random.uniform(-0.3, 0.3), 2)
        sgpa_trend = round(prev_sgpa - avg_sgpa, 2)

        avg_marks = round(random.uniform(45, 90), 2)

        # --- Feedback attributes ---
        avg_difficulty = round(random.uniform(1.5, 4.5), 2)   # 1–5
        avg_study_hours = round(random.uniform(1.0, 6.0), 2)
        planned_effort = random.randint(1, 5)

        # --- Generate next SGPA (target) ---
        next_sgpa = (
            0.45 * prev_sgpa +
            0.15 * avg_sgpa +
            0.15 * (avg_marks / 10) +
            0.10 * avg_study_hours +
            0.10 * planned_effort -
            0.10 * avg_difficulty +
            random.uniform(-0.2, 0.2)
        )

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


df = generate_initial_dataset(500)
print(df.head())

# Save 
df.to_csv("initial_dataset.csv", index=False)
