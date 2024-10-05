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
    
    # Append the results to the list
    results.append({
        'Star Index': index,
        'RA (degrees)': ra,
        'Dec (degrees)': dec,
        'Distance (AU)': distance
    })

# Create a DataFrame from the results
results_df = pd.DataFrame(results)

# Save the DataFrame to a new CSV file
results_df.to_csv('ra_de_data.csv', index=True)

print('Astrometric data for all stars has been saved to calculated_stars_data.csv.')
print('Total stars processed:', len(filtered_stars_df))
