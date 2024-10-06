import pandas as pd
import numpy as np

# Load the astrometric data from the CSV files
ra_de_data_df = pd.read_csv('color_coded.csv')
pla2sun_df = pd.read_csv('pla2sun.csv')  # Load planet-to-sun data

# Convert RA and Dec columns to numeric types
ra_de_data_df['RA (degrees)'] = pd.to_numeric(ra_de_data_df['RA (degrees)'], errors='coerce')
ra_de_data_df['Dec (degrees)'] = pd.to_numeric(ra_de_data_df['Dec (degrees)'], errors='coerce')
ra_de_data_df['Magnitude'] = pd.to_numeric(ra_de_data_df['Magnitude'], errors='coerce')  # Ensure magnitude is numeric
ra_de_data_df['Color'] = pd.to_numeric(ra_de_data_df['Color'], errors='coerce')  # Convert B-V to numeric
ra_de_data_df['Star HIP'] = pd.to_numeric(ra_de_data_df['Star HIP'], errors='coerce').astype('Int64')

def equatorial_to_cartesian(ra_degrees, dec_degrees, distance_au):
    distance_meters = distance_au * 1.496e11  # 1 AU is approximately 1.496 x 10^11 meters
    ra_radians = np.radians(ra_degrees)
    dec_radians = np.radians(dec_degrees)
    x = distance_meters * np.cos(dec_radians) * np.cos(ra_radians)
    y = distance_meters * np.cos(dec_radians) * np.sin(ra_radians)
    z = distance_meters * np.sin(dec_radians)
    return x, y, z

# Check if 'Star HIP' column exists in ra_de_data_df
if 'Star HIP' not in ra_de_data_df.columns:
    print("Warning: 'Star HIP' column not found in ra_de_data_df.")

# Iterate over each planet in pla2sun_df
for index, planet_row in pla2sun_df.iterrows():
    planet_name = planet_row['pl_name']  # Get the planet name
    planet_radius = planet_row['radius']  # Get the planet radius

    # Convert each star's RA, Dec, and distance to Cartesian coordinates
    ra_de_data_df[['x_f', 'y_f', 'z_f']] = ra_de_data_df.apply(
        lambda row: equatorial_to_cartesian(row['RA (degrees)'], row['Dec (degrees)'], row['Distance (AU)']),
        axis=1,
        result_type='expand'
    )

    # Calculate positions relative to the current planet
    ra_de_data_df['xx'] = ra_de_data_df['x_f'] - planet_row['absolute_x']
    ra_de_data_df['yy'] = ra_de_data_df['y_f'] - planet_row['absolute_y']
    ra_de_data_df['zz'] = ra_de_data_df['z_f'] - planet_row['absolute_z']

    # Merge to get host star HIP using the correct column name
    merged_df = ra_de_data_df.merge(pla2sun_df[['hip', 'pl_name']], left_on='Star HIP', right_on='hip', how='left')

    # Prepare the output DataFrame with relevant columns, placing HIP first
    output_df = merged_df[['Star HIP', 'RA (degrees)', 'Dec (degrees)', 'Magnitude', 'Color', 'xx', 'yy', 'zz']].copy()
    output_df['pl_name'] = planet_name  # Add planet name to the output DataFrame

    # Save the output DataFrame to CSV
    output_df.to_csv(f'{planet_name}.csv', index=False)

    print(f'Output for {planet_name} saved to {planet_name}.csv')