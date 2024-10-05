import pandas as pd
import matplotlib.pyplot as plt
from math import radians, degrees, asin
import numpy as np

# Load the astrometric data from the CSV file
ra_de_data_df = pd.read_csv('color_coded.csv')

# Convert RA and Dec columns to numeric types (in case they're strings)
ra_de_data_df['RA (degrees)'] = pd.to_numeric(ra_de_data_df['RA (degrees)'], errors='coerce')
ra_de_data_df['Dec (degrees)'] = pd.to_numeric(ra_de_data_df['Dec (degrees)'], errors='coerce')
ra_de_data_df['Magnitude'] = pd.to_numeric(ra_de_data_df['Magnitude'], errors='coerce')  # Ensure magnitude is numeric
ra_de_data_df['Color'] = pd.to_numeric(ra_de_data_df['Color'], errors='coerce')  # Convert B-V to numeric

# Function to convert B-V color index to RGB
def bv_to_rgb(bv):
    # Define RGB values for some B-V ranges
    if bv <= -0.30:    # Blue
        return (0.0, 0.0, 1.0)  # Blue
    elif -0.30 < bv <= 0.0:     # Blue-White
        return (0.5, 0.5, 1.0)  # Light Blue
    elif 0.0 < bv <= 0.30:      # White
        return (1.0, 1.0, 1.0)  # White
    elif 0.30 < bv <= 0.60:     # Yellow-White
        return (1.0, 1.0, 0.5)  # Light Yellow
    elif 0.60 < bv <= 1.0:      # Yellow
        return (1.0, 1.0, 0.0)  # Yellow
    elif 1.0 < bv <= 1.5:       # Orange
        return (1.0, 0.5, 0.0)  # Orange
    else:                        # Red
        return (1.0, 0.0, 0.0)  # Red

# Get GPS coordinates and elevation
gps_latitude = 40.7128  # Latitude (degrees)
gps_longitude = -74.0060  # Longitude (degrees)
observer_elevation = 5  # Elevation (meters)

# Constants
R = 6371000  # Radius of the Earth in meters

# Calculate the visible declination based on observer's elevation
visible_declination = 90 - degrees(asin(R / (R + observer_elevation)))

# Prepare list to store star map data
star_map_data = []

# Iterate over each star in the DataFrame
for index, row in ra_de_data_df.iterrows():
    ra = row['RA (degrees)']  # Right Ascension in degrees
    dec = row['Dec (degrees)']  # Declination in degrees
    magnitude = row['Magnitude']  # Star's magnitude
    color_value = row['Color']  # B-V color index
    
    # Apply elevation control (only include stars above the observer's horizon)
    if dec >= visible_declination:
        # Adjust size based on magnitude (you can customize the scaling factor)
        size = -4.975 * magnitude + 24.975  # Size mapping from magnitude to size
        size = max(size, 0.1)  # Invert magnitude for size (size is from 0.1 to 20)
        
        # Convert B-V to RGB
        color = bv_to_rgb(color_value)
        
        star_map_data.append((ra, dec, size, color))

# Plot the star map
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_direction(-1)  # To match traditional star chart orientation
ax.set_theta_offset(radians(gps_longitude))

# Convert RA and Dec to polar coordinates for the map
for star in star_map_data:
    ra, dec, size, color = star
    # RA corresponds to azimuth (theta), Dec corresponds to radius (r)
    theta = radians(ra)  # Azimuth (RA in radians)
    r = 90 - dec         # Radius (inverted Dec for correct projection)

    glow_size = size * 2.5  # Make the glow larger than the star
    ax.scatter(theta, r, color=(*color, 0.2), s=glow_size, alpha=0.5)
    
    # Plot the star on the map with variable size and color
    ax.scatter(theta, r, color=color, s=size)  # 's' specifies the size

# Customize the plot (night sky-like background)
ax.set_facecolor('black')
ax.grid(False)
ax.set_yticklabels([])  # Hide radial (Dec) labels
ax.set_xticklabels([])  # Hide angular (RA) labels

plt.title(f'Star Map (Observer on the Sun at {gps_latitude}°N, {gps_longitude}°E, Elevation: {observer_elevation} m)')
plt.show()
