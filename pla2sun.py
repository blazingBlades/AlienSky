import pandas as pd
import numpy as np
from skyfield.api import Star, load
from skyfield.data import hipparcos

# Load the CSV files
hip_data = pd.read_csv('hipdis.csv')  # Contains host star information with distance in AU
planet_data = pd.read_csv('planet_positions.csv')  # Contains planet positions in meters

# Function to convert equatorial coordinates to Cartesian coordinates using distance in AU
def equatorial_to_cartesian(ra_degrees, dec_degrees, distance_au):
    # Convert distance from AU to meters
    distance_meters = distance_au * 1.496e11  # 1 AU is approximately 1.496 x 10^11 meters

    # Convert angles to radians
    ra_radians = np.radians(ra_degrees)
    dec_radians = np.radians(dec_degrees)

    # Calculate Cartesian coordinates in meters
    x = distance_meters * np.cos(dec_radians) * np.cos(ra_radians)
    y = distance_meters * np.cos(dec_radians) * np.sin(ra_radians)
    z = distance_meters * np.sin(dec_radians)

    return x, y, z

# Convert each star's RA, Dec, and distance to Cartesian coordinates
hip_data[['x_star', 'y_star', 'z_star']] = hip_data.apply(
    lambda row: equatorial_to_cartesian(row['RA (degrees)'], row['Dec (degrees)'], row['Distance (AU)']),
    axis=1,
    result_type='expand'
)

print(hip_data)

# Rename the 'hip' column for clarity
hip_data.rename(columns={'hip': 'hip'}, inplace=True)

# Merge the datasets on 'hip' to get the star positions
merged_data = pd.merge(planet_data, hip_data, on='hip', how='inner')

# Calculate the absolute position of the planet from the Sun (convert star position from parsecs to meters)
def calculate_absolute_position(row):
    # Conversion factor from parsecs to meters
    #parsec_to_meters = 3.0857e16
    
    star_x = row['x_star'] #* parsec_to_meters
    star_y = row['y_star'] #* parsec_to_meters
    star_z = row['z_star'] #* parsec_to_meters
    
    planet_x = row['x']
    planet_y = row['y']
    planet_z = row['z']
    
    absolute_x = star_x + planet_x
    absolute_y = star_y + planet_y
    absolute_z = star_z + planet_z
    return pd.Series([absolute_x, absolute_y, absolute_z])

# Apply the calculation to get the absolute position of the planet
merged_data[['absolute_x', 'absolute_y', 'absolute_z']] = merged_data.apply(calculate_absolute_position, axis=1)

# Function to create rotation matrix from angles (in degrees)
def rotation_matrix(true_anomaly, inclination):
    true_anomaly_rad = np.radians(true_anomaly)
    inclination_rad = np.radians(inclination)

    # Rotation about the Z-axis (for true anomaly)
    Rz = np.array([[np.cos(true_anomaly_rad), -np.sin(true_anomaly_rad), 0],
                   [np.sin(true_anomaly_rad), np.cos(true_anomaly_rad), 0],
                   [0, 0, 1]])

    # Rotation about the Y-axis (for inclination)
    Ry = np.array([[np.cos(inclination_rad), 0, np.sin(inclination_rad)],
                   [0, 1, 0],
                   [-np.sin(inclination_rad), 0, np.cos(inclination_rad)]])

    # Combined rotation
    R = np.dot(Ry, Rz)
    return R

# Calculate SE(3) for each planet
def calculate_SE3(row):
    # Get the absolute position
    position = np.array([row['absolute_x'], row['absolute_y'], row['absolute_z']])

    # Get the orientation (rotation matrix)
    R = rotation_matrix(row['true_anomaly'], row['inclination'])

    # Create the SE(3) matrix (4x4)
    SE3 = np.eye(4)
    SE3[:3, :3] = R  # Assign rotation
    SE3[:3, 3] = position  # Assign translation

    return SE3

# Calculate SE(3) for each planet and store in a new column
merged_data['SE3'] = merged_data.apply(calculate_SE3, axis=1)

# For simplicity, convert SE(3) matrices to string format for CSV output
merged_data['SE3_string'] = merged_data['SE3'].apply(lambda x: x.tolist())  # Convert to list for easy saving

# Select relevant columns for output
output_data = merged_data[['pl_name', 'hostname', 'radius','hip', 'absolute_x', 'absolute_y', 'absolute_z', 
                            'true_anomaly', 'inclination', 'SE3_string']]

# Save the results to a new CSV file
output_data.to_csv('pla2sun.csv', index=False)

print("SE(3) representation of planets from the Sun calculated and saved to 'pla2sun.csv'.")
