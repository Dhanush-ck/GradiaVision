import pandas as pd

def remove_duplicates(input_file, output_file):
    # Load the dataset
    df = pd.read_csv(input_file)
    
    # 1. Identify duplicates (excluding the first occurrence)
    # This gives us a boolean mask where True = is a duplicate
    duplicate_mask = df.duplicated(keep='first')
    
    # Get the line numbers of duplicates (adding 2 because of 0-indexing and header)
    duplicate_indices = df[duplicate_mask].index.tolist()
    duplicate_line_nums = [i + 2 for i in duplicate_indices]
    
    if len(duplicate_line_nums) > 0:
        print(f"Found {len(duplicate_line_nums)} duplicate lines.")
        print(f"Removing lines: {duplicate_line_nums}")
        
        # 2. Remove duplicates and keep only the first instance
        # df_cleaned = df.drop_duplicates(keep='first')
        
        # # 3. Save the clean file
        # df_cleaned.to_csv(output_file, index=False)
        # print(f"Cleaned file saved as: {output_file}")
    else:
        print("No duplicates found. File is already clean.")

# Usage
remove_duplicates('intent_dataset.csv', 'intent_dataset_new.csv')