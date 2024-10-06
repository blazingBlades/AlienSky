import pandas as pd
import matplotlib.pyplot as plt
from math import radians, degrees, asin
import numpy as np

# Load the astrometric data from the CSV files
ra_de_data_df = pd.read_csv('color_coded.csv')
pla2sun_df = pd.read_csv('pla2sun.csv')  # Load planet-to-sun data

planet_no = 21
# Change the index here if you want a different planet ##0-24 max
# Convert RA and Dec columns to numeric types (in case they're strings)
ra_de_data_df['RA (degrees)'] = pd.to_numeric(ra_de_data_df['RA (degrees)'], errors='coerce')
ra_de_data_df['Dec (degrees)'] = pd.to_numeric(ra_de_data_df['Dec (degrees)'], errors='coerce')
ra_de_data_df['Magnitude'] = pd.to_numeric(ra_de_data_df['Magnitude'], errors='coerce')  # Ensure magnitude is numeric
ra_de_data_df['Color'] = pd.to_numeric(ra_de_data_df['Color'], errors='coerce')  # Convert B-V to numeric

# Get the planet radius from the first row (or specify the index of the planet you want)
planet_row = pla2sun_df.iloc[planet_no]  
planet_r = planet_row['radius']

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
ra_de_data_df[['x_f', 'y_f', 'z_f']] = ra_de_data_df.apply(
    lambda row: equatorial_to_cartesian(row['RA (degrees)'], row['Dec (degrees)'], row['Distance (AU)']),
    axis=1,
    result_type='expand'
)

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

# Get GPS coordinates and elevation
gps_latitude = 35.011665  # Latitude (degrees) ##kyoto
gps_longitude = 135.768326  # Longitude (degrees) ###kyoto
observer_elevation = 0  # Elevation (meters)

# Constants
R = 6371000 * planet_r  # Radius of the Earth in meters * ratio

# Calculate the visible declination based on observer's elevation
visible_declination = 90 - degrees(asin(R / (R + observer_elevation)))

# Calculate zenith angle for the observer
zenith_angle = 90 - (visible_declination + gps_latitude)

# Prepare list to store star map data
star_map_data = []

# Iterate over each star in the DataFrame
for star_index, star_row in ra_de_data_df.iterrows():
    ra = star_row['RA (degrees)']  # Right Ascension in degrees
    dec = star_row['Dec (degrees)']  # Declination in degrees
    magnitude = star_row['Magnitude']  # Star's magnitude
    color_value = star_row['Color']  # B-V color index
    
    # Apply elevation control (only include stars above the observer's horizon)
    if dec >= (visible_declination - zenith_angle):  # Adjust visibility based on zenith angle
        # Adjust size based on magnitude
        size = -4.975 * magnitude + 24.975
        size = max(size, 0.1)  # Invert magnitude for size
        
        # Convert B-V to RGB
        color = bv_to_rgb(color_value)

        xx = star_row['x_f'] - planet_row['absolute_x']
        yy = star_row['y_f'] - planet_row['absolute_y']
        zz = star_row['z_f'] - planet_row['absolute_z']

        # Calculate star position in Cartesian coordinates (in AU)
        dec = np.degrees(np.arcsin(zz / np.sqrt(xx**2 + yy**2 + zz**2)))

        # Calculate RA in degrees
        ra = np.degrees(np.arctan2(yy, xx))

        # Ensure RA is in the range [0, 360)
        if ra < 0:
            ra += 360

        # Store transformed position with star data
        star_map_data.append((xx, yy, zz, size, color))

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
ax.set_xticklabels([])  # Hide

plt.title(f'Star Map (Observer on {planet_row["pl_name"]} at {gps_latitude}°N, {gps_longitude}°E, Elevation: {observer_elevation} m)')
plt.show()
