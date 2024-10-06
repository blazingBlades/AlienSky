from skyfield.api import Star, load
from skyfield.data import hipparcos
import pandas as pd

# Load the Hipparcos star data
with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)

# Print the available columns in the DataFrame
print(df.columns)

# Filter the DataFrame to remove rows with null RA
df = df[df['ra_degrees'].notnull()]

# Check for a spectral type column
# Uncomment the next line to see the first few rows of the DataFrame for inspection
# print(df.head())

# Define a function to map spectral types to colors
def spectral_type_to_color(spectral_type):
    if pd.isnull(spectral_type):
        return "Unknown"
    spectral_type = spectral_type.strip()
    if spectral_type.startswith('O'):
        return "Blue"
    elif spectral_type.startswith('B'):
        return "Blue-White"
    elif spectral_type.startswith('A'):
        return "White"
    elif spectral_type.startswith('F'):
        return "Yellow-White"
    elif spectral_type.startswith('G'):
        return "Yellow"
    elif spectral_type.startswith('K'):
        return "Orange"
    elif spectral_type.startswith('M'):
        return "Red"
    else:
        return "Unknown"

# Check if there is a relevant column for spectral types
# The actual column name might differ
# Replace 'spectral_type' with the correct name if found
if 'spectral_type' in df.columns:
    # Add a new column to the DataFrame for color
    df['color'] = df['spectral_type'].apply(spectral_type_to_color)
else:
    print("No 'spectral_type' column found in the DataFrame.")

# Select a specific star
tar_star = Star.from_dataframe(df.loc[87937])

# Load planetary data
planets = load('de421.bsp')
sun = planets['sun']

# Create a timescale and get the current time
ts = load.timescale()
t = ts.now()
# t = ts.utc(2010, 9, 3) for exact time

# Calculate astrometric position
astrometric = sun.at(t).observe(tar_star)
ra, dec, distance = astrometric.radec()

# Convert RA and Dec to decimal degrees
ra_degrees = ra.hours * 15  # Convert RA from hours to degrees
dec_degrees = dec.degrees    # Get Dec in degrees

# Get the color of the selected star if color is added
star_color = df.loc[87937, 'color'] if 'color' in df.columns else "Color not available"

# Print the results
print(f"RA (degrees): {ra_degrees:.6f}")
print(f"Dec (degrees): {dec_degrees:.6f}")
print(f"Distance (AU): {distance.au:.6e}")  # Access distance in AU
print(f"Star Color: {star_color}")

# Filter the DataFrame for stars with magnitude <= 5
df = df[df['magnitude'] <= 5]  # Brightness filtering (6 because it is the naked-eye limit)
print('After filtering, there are {} stars'.format(len(df)))
