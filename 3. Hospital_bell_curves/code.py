import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------- File paths ----------
summary_file = "summary_stats.csv"
raw_data_file = "raw_data.xlsx"
hospital_col = "Admission Hospital Name"
reach_col = "Hospital Reach Time"
start_col = "Hospital Start Time"
output_folder = "hospital_bell_curves"

# ---------- Step 1: Read hospital names from summary CSV ----------
summary_df = pd.read_csv(r'c:\Users\preri\Desktop\Project Hospital Wait statistics\2. Small and Big hospitals(avg per day one case)\count_more_than_181.csv')
hospital_names = summary_df[hospital_col].dropna().unique()

# ---------- Step 2: Load raw data and clean ----------
raw_df = pd.read_csv(r'c:\Users\preri\Desktop\Project Hospital Wait statistics\Raw and cleaned data\cleaned_file.csv')
raw_df.columns = raw_df.columns.str.strip()

# Standardize hospital names to uppercase
raw_df[hospital_col] = raw_df[hospital_col].str.strip().str.upper()

# Parse datetime columns
raw_df[reach_col] = pd.to_datetime(raw_df[reach_col], errors='coerce', dayfirst=False)
raw_df[start_col] = pd.to_datetime(raw_df[start_col], errors='coerce', dayfirst=False)

# Calculate duration in minutes
raw_df['Duration (min)'] = (raw_df[start_col] - raw_df[reach_col]).dt.total_seconds() / 60

# Drop rows with missing or negative duration
raw_df = raw_df[raw_df['Duration (min)'].notna() & (raw_df['Duration (min)'] >= 0)]

# ---------- Step 3: Create output folder ----------
os.makedirs(output_folder, exist_ok=True)

# ---------- Step 4: Generate bell curves ----------
for hospital in hospital_names:
    hospital_upper = hospital.strip().upper()
    hospital_data = raw_df[raw_df[hospital_col] == hospital_upper]

    if hospital_data.empty:
        print(f"⚠️ No matching data for: {hospital_upper}")
        continue

    durations = hospital_data['Duration (min)'].dropna()

    if len(durations) < 5:
        print(f"⚠️ Not enough data to plot for: {hospital_upper}")
        continue

    # Plot
    plt.figure(figsize=(8, 5))
    sns.histplot(durations, kde=True, stat='density', bins=30, color='skyblue')
    plt.title(f'Bell Curve - {hospital_upper}')
    plt.xlabel('Duration (min)')
    plt.ylabel('Density')

    # Save
    safe_name = hospital_upper.replace("/", "_").replace(" ", "_")
    output_path = os.path.join(output_folder, f"{safe_name}.png")
    plt.savefig(output_path)
    plt.close()

    print(f"✅ Saved: {output_path}")

print("\n🎉 All bell curves saved in folder:", output_folder)
