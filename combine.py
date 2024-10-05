import pandas as pd

# Load the original star data CSV
original_df = pd.read_csv('ra_de_data.csv')

# Load the color data CSV
color_df = pd.read_csv('hip_color.csv')

# Merge the two DataFrames on 'Star HIP'
combined_df = pd.merge(original_df, color_df, on='Star HIP', how='left')

# Save the combined DataFrame to a new CSV
combined_df.to_csv('color_coded.csv', index=False)
print("Combined CSV file saved as 'color_coded.csv'.")
