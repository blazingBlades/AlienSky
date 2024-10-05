import pandas as pd

# Load the CSV files
hip_data = pd.read_csv('color_coded.csv')  # Adjust the path if needed
planet_position = pd.read_csv('planet_positions.csv')  # Adjust the path if needed

# Extract the 'hip' values from hip_data
hip_values = hip_data['Star HIP'].unique()

planet_position = planet_position.sort_values(by= 'hip')

# Filter the planet_position DataFrame
filtered_planet_position = planet_position[planet_position['hip'].isin(hip_values)]

# Display the filtered DataFrame (optional)
#print(filtered_planet_position)

# Save the filtered results to a new CSV file (optional)
filtered_planet_position.to_csv('fil_planet.csv', index=False)
