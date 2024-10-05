import pandas as pd
from skyfield.api import load
from skyfield.data import hipparcos

# Load the Hipparcos data
# Replace with your actual data loading mechanism if needed
with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)

# Step 1: Remove rows with null RA values
df = df[df['ra_degrees'].notnull()]

# Load the exhip.csv file to get the list of HIP IDs
exhip_df = pd.read_csv('exhip.csv')  # Adjust the path if needed

# Ensure that the column containing the HIP IDs in exhip.csv is named correctly
hip_ids = exhip_df['hip'].unique()  # Adjust column name if necessary

# Step 4: Filter to keep only rows with HIP IDs present in exhip.csv
df_filtered = df[df.index.isin(hip_ids)]

df_filtered.to_csv('hip_rd.csv', index=True)


