import pandas as pd

# Load your file
df = pd.read_csv('intent_dataset.csv')

# 1. Separate the majority and minority classes
df_majority = df[df.intent == 'target_percentage']
df_minorities = df[df.intent != 'target_percentage']

# 2. Downsample the majority class to match the average of others (~100)
# You can change 'n=100' to whatever number you prefer
df_majority_downsampled = df_majority.sample(n=100, random_state=42)

# 3. Combine them back together
df_balanced = pd.concat([df_majority_downsampled, df_minorities])

# 4. Shuffle the data (Very important for Logistic Regression!)
df_balanced = df_balanced.sample(frac=1).reset_index(drop=True)

# Save the new balanced dataset
df_balanced.to_csv('balanced_intent_dataset.csv', index=False)

print("New Distribution:")
print(df_balanced['intent'].value_counts())