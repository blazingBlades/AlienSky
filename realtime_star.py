import pandas as pd
from skyfield.api import Star, load

# Load the filtered CSV file
filtered_stars_df = pd.read_csv('hip_data_l6.csv')

# Load planetary data
planets = load('de421.bsp')
sun = planets['sun']

# Create a timescale and get the current time
ts = load.timescale()
t = ts.now()

# Prepare a list to hold the results
results = []

# Iterate over each star in the filtered DataFrame
for index, row in filtered_stars_df.iterrows():
    tar_star = Star.from_dataframe(row)
    
    # Calculate astrometric position
    astrometric = sun.at(t).observe(tar_star)
    ra, dec, distance = astrometric.radec()
    
    # Convert RA and Dec to decimal degrees
    ra_degrees = ra.hours * 15  # Convert from hours to degrees (15 degrees per hour)
    dec_degrees = dec.degrees   # Already in degrees

    # Append the results to the list
    results.append({
        'Star HIP': row['hip'],
        'Magnitude': row['magnitude'],
        'RA (degrees)': ra_degrees,
        'Dec (degrees)': dec_degrees,
        'Distance (AU)': distance.au
    })

# Create a DataFrame from the results
results_df = pd.DataFrame(results)

# Save the DataFrame to a new CSV file
results_df.to_csv('ra_de_data.csv', index=False)

print('Astrometric data for all stars has been saved to ra_de_data.csv.')
print('Total stars processed:', len(filtered_stars_df))
