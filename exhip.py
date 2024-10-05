import pandas as pd

# Load the CSV file
planet_position = pd.read_csv('planet_positions.csv')  # Adjust the path if needed

# Extract only the 'hip' column
hip_only = planet_position[['hip']]

hip_only = hip_only.sort_values(by= 'hip')

# Save the extracted 'hip' column to a new CSV file
hip_only.to_csv('exhip.csv', index=False)
