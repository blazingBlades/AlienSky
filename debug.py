import pandas as pd
import matplotlib.pyplot as plt
from math import radians, degrees, asin
import numpy as np

# Load the astrometric data from the CSV files
ra_de_data_df = pd.read_csv('color_coded.csv')
pla2sun_df = pd.read_csv('pla2sun.csv')  # Load planet-to-sun data

planet_no = 21  # Change the index here if you want a different planet

# Convert RA and Dec columns to numeric types (in case they're strings)
ra_de_data_df['RA (degrees)'] = pd.to_numeric(ra_de_data_df['RA (degrees)'], errors='coerce')
ra_de_data_df['Dec (degrees)'] = pd.to_numeric(ra_de_data_df['Dec (degrees)'], errors='coerce')
ra_de_data_df['Magnitude'] = pd.to_numeric(ra_de_data_df['Magnitude'], errors='coerce')  # Ensure magnitude is numeric
ra_de_data_df['Color'] = pd.to_numeric(ra_de_data_df['Color'], errors='coerce')  # Convert B-V to numeric

# Get the planet radius from the selected row
planet_row = pla2sun_df.iloc[planet_no]  
planet_r = planet_row['radius']

# Constants
AU_TO_METERS = 1.496e11  # 1 AU in meters
R = 6371000 * planet_r  # Radius of the planet in meters

# Function to convert B-V color index to RGB
def bv_to_rgb(bv):
    if bv <= -0.30:    # Blue
        return (0.0, 0.0, 1.0)
    elif -0.30 < bv <= 0.0:     # Blue-White
        return (0.5, 0.5, 1.0)
    elif 0.0 < bv <= 0.30:      # White
        return (1.0, 1.0, 1.0)
    elif 0.30 < bv <= 0.60:     # Yellow-White
        return (1.0, 1.0, 0.5)
    elif 0.60 < bv <= 1.0:      # Yellow
        return (1.0, 1.0, 0.0)
    elif 1.0 < bv <= 1.5:       # Orange
        return (1.0, 0.5, 0.0)
    else:                        # Red
        return (1.0, 0.0, 0.0)

# Extract SE3 transformation from the selected planet row
def extract_se3(se3_string):
    try:
        # Convert the SE3_string directly to a numpy array
        matrix = np.array(eval(se3_string))  # Assuming the string is a valid 4x4 matrix
        if matrix.shape != (4, 4):
            raise ValueError("SE3_string is not a 4x4 matrix")
        
        R = matrix[:3, :3]  # Extract the rotation part (3x3)
        t = matrix[:3, 3]   # Extract the translation part (3x1)
        return R, t
    except Exception as e:
        raise ValueError(f"Error extracting SE3: {e}")

# Get GPS coordinates and elevation
gps_latitude = 40.7128  # Latitude (degrees)
gps_longitude = -74.0060  # Longitude (degrees)
observer_elevation = 5  # Elevation (meters)

# Calculate the visible declination based on observer's elevation
visible_declination = 90 - degrees(asin(R / (R + observer_elevation)))

# Prepare list to store star map data
star_map_data = []

# Process the selected planet
se3_string = planet_row['SE3_string']
R_matrix, t_vector = extract_se3(se3_string)

# Iterate over each star in the DataFrame
for star_index, star_row in ra_de_data_df.iterrows():
    ra = star_row['RA (degrees)']  # Right Ascension in degrees
    dec = star_row['Dec (degrees)']  # Declination in degrees
    magnitude = star_row['Magnitude']  # Star's magnitude
    color_value = star_row['Color']  # B-V color index
    
    # Apply elevation control (only include stars above the observer's horizon)
    if dec >= visible_declination:
        # Adjust size based on magnitude
        size = -4.975 * magnitude + 24.975
        size = max(size, 0.1)  # Invert magnitude for size
        
        # Convert B-V to RGB
        color = bv_to_rgb(color_value)

        # Calculate star position in Cartesian coordinates (in AU)
        star_x_au = np.cos(radians(dec)) * np.cos(radians(ra))  # x = cos(Dec) * cos(RA)
        star_y_au = np.cos(radians(dec)) * np.sin(radians(ra))  # y = cos(Dec) * sin(RA)
        star_z_au = np.sin(radians(dec))  # z = sin(Dec)

        # Convert star position from AU to meters
        star_x_m = star_x_au * AU_TO_METERS
        star_y_m = star_y_au * AU_TO_METERS
        star_z_m = star_z_au * AU_TO_METERS

        # Transform star position to the planet's reference frame
        star_position = np.array([star_x_m, star_y_m, star_z_m])
        transformed_position = R_matrix @ star_position + t_vector  # Apply SE3 transformation
        
        # Store transformed position with star data
        star_map_data.append((*transformed_position, size, color))

# Plot the star map
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_direction(-1)  # To match traditional star chart orientation
ax.set_theta_offset(radians(gps_longitude))

# Convert transformed star positions to polar coordinates for the map
for star in star_map_data:
    x, y, z, size, color = star
    # Convert the transformed positions to RA and Dec
    ra = degrees(np.arctan2(y, x))
    dec = degrees(np.arcsin(z / np.sqrt(x**2 + y**2 + z**2)))
    
    theta = radians(ra)  # Azimuth (RA in radians)
    r = 90 - dec         # Radius (inverted Dec for correct projection)

    glow_size = size * 0.3  # Make the glow larger than the star
    ax.scatter(theta, r, color=(*color, 0.3), s=glow_size, alpha=0.5)
    
    # Plot the star on the map with variable size and color
    ax.scatter(theta, r, color=(1.0, 1.0, 1.0), s=size * 0.1)  # 's' specifies the size

# Customize the plot (night sky-like background)
ax.set_facecolor('black')
ax.grid(False)
ax.set_yticklabels([])  # Hide radial (Dec) labels
ax.set_xticklabels([])  # Hide angular (RA) labels

plt.title(f'Star Map (Observer on the Sun at {gps_latitude}°N, {gps_longitude}°E, Elevation: {observer_elevation} m)')
plt.show()
