import pandas as pd
import numpy as np
from scipy import stats

# Load data
df = pd.read_csv('cleaned_file.csv', dtype=str)

# Convert time columns
df['Hospital Reach Time'] = pd.to_datetime(df['Hospital Reach Time'], errors='coerce')
df['Hospital Start Time'] = pd.to_datetime(df['Hospital Start Time'], errors='coerce')

# Clean hospital names
df['Admission Hospital Name'] = df['Admission Hospital Name'].astype(str).str.strip()

# Compute waiting time in minutes
df['Waiting Time (min)'] = (df['Hospital Start Time'] - df['Hospital Reach Time']).dt.total_seconds() / 60

# Drop invalid rows
df = df[df['Waiting Time (min)'] >= 0]

# Round to nearest minute
df['Waiting Time (rounded)'] = df['Waiting Time (min)'].round().astype(int)

# Define function to compute mode from rounded values
def mode_from_rounded(series):
    if series.empty:
        return np.nan
    return series.value_counts().idxmax()

# Group and compute stats
grouped = df.groupby('Admission Hospital Name')

summary = grouped['Waiting Time (min)'].agg([
    ('count', 'count'),
    ('mean (min)', 'mean'),
    ('median (min)', 'median'),
    ('std dev (min)', 'std'),
    ('min (min)', 'min'),
    ('max (min)', 'max'),
    ('25th percentile (min)', lambda x: np.percentile(x, 25)),
    ('75th percentile (min)', lambda x: np.percentile(x, 75)),
])

# Add mode based on rounded values
summary['mode (rounded to nearest min)'] = grouped['Waiting Time (rounded)'].apply(mode_from_rounded)

# Round numeric columns
summary = summary.round(2)

# Show summary
print(summary)

summary.to_excel('hospital_wait_time_summary.xlsx')
