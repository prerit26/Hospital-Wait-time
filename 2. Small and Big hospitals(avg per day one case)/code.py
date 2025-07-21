import pandas as pd

# Step 1: Read the Excel file
df = pd.read_excel("hospital_wait_time_summary.xlsx")  # Replace with your actual file name

# Step 2: Clean column names
df.columns = df.columns.str.strip()

# Step 3: Ensure 'count' is numeric
df['count'] = pd.to_numeric(df['count'], errors='coerce')

# Step 4: Split the data
group_high = df[df['count'] > 181]
group_low = df[df['count'] <= 181]

# Step 5: Save to CSV files
group_high.to_csv("count_more_than_181.csv", index=False)
group_low.to_csv("count_less_equal_181.csv", index=False)

print("Saved:")
print("- count_more_than_181.csv")
print("- count_less_equal_181.csv")
