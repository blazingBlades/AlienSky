import pandas as pd

# Example of loading a DataFrame from a CSV file
df = pd.read_csv('ra_de_data.csv')

# Check the first few rows of the DataFrame
print(df.head())

import numpy as np

# Convert RA and Dec from degrees to radians
df['RA (degrees)'] = np.deg2rad(df['RA'])
df['Dec_rad'] = np.deg2rad(df['Dec'])

# Apply the transformation formulas
df['x'] = df['Distance'] * np.cos(df['Dec_rad']) * np.cos(df['RA_rad'])
df['y'] = df['Distance'] * np.cos(df['Dec_rad']) * np.sin(df['RA_rad'])
df['z'] = df['Distance'] * np.sin(df['Dec_rad'])

# Show the updated DataFrame with Cartesian coordinates
print(df[['HIP', 'x', 'y', 'z']])
