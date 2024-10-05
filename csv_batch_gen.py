from astroquery.vizier import Vizier
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import time  # Import the time module

# Set the catalog and file output
catalog = "I/355/gaiadr3"  # Gaia DR3 catalog
output_file = "gaia_batch_abs_mag.csv"

# Function to calculate absolute magnitude from apparent magnitude and parallax
def calculate_absolute_magnitude(apparent_magnitude, parallax):
    if parallax > 0:  # Avoid division by zero
        distance = 1 / (parallax / 1000)  # Convert parallax from mas to arcseconds and then to parsecs
        abs_mag = apparent_magnitude - 5 * (np.log10(distance) - 1)
        return abs_mag
    else:
        return None  # Return None if parallax is zero or negative

# Function to query the database
def query_hip(hip_id):
    # Specify only the columns you need (e.g., RAJ2000, DEJ2000, Gmag, Plx, Teff)
    result = Vizier.query_constraints(catalog=catalog, HIP=str(hip_id), columns=['RAJ2000', 'DEJ2000', 'Gmag', 'Plx', 'Teff', 'PM'])
    if result:
        # Check if result[0] has multiple rows and take the first one
        data = result[0]
        if len(data) > 0:
            apparent_magnitude = data['Gmag'][0] if 'Gmag' in data.columns else None
            parallax = data['Plx'][0] if 'Plx' in data.columns else None  # Parallax in milliarcseconds
            teff = data['Teff'][0] if 'Teff' in data.columns else None
            pm = data['PM'][0] if 'PM' in data.columns else None
            
            # Calculate absolute magnitude
            abs_mag = calculate_absolute_magnitude(apparent_magnitude, parallax)

            return hip_id, {
                'RAJ2000': data['RAJ2000'][0] if 'RAJ2000' in data.columns else None,
                'DEJ2000': data['DEJ2000'][0] if 'DEJ2000' in data.columns else None,
                'Gmag': apparent_magnitude,
                'Plx': parallax,
                'Teff': teff,
                'PM': pm
            }, abs_mag  # Return HIP ID, data, and absolute magnitude
            
    return hip_id, None, None  # Return HIP ID and None if no data is found

# Record the start time
start_time = time.time()

# Open the CSV file for writing
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["HIP ID", "RAJ2000", "DEJ2000", "Gmag", "Plx", "Teff", "PM", "Absolute Magnitude"])  # Write header with specific columns

    # Use ThreadPoolExecutor to parallelize the queries
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        futures = []

        # Loop over HIP IDs in range
        for hip_id in range(1, 1000):  # Adjust to the desired range
            futures.append(executor.submit(query_hip, hip_id))  # Submit each HIP ID for querying

        for future in as_completed(futures):
            hip_id, data, abs_mag = future.result()
            if data is None:  # Check if data is None
                writer.writerow([hip_id, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"])  # Write HIP ID with "NULL"
            else:
                # Write HIP ID and relevant data, ensuring data is accessed correctly
                writer.writerow([
                    hip_id,
                    data['RAJ2000'] if data['RAJ2000'] is not None else "NULL",
                    data['DEJ2000'] if data['DEJ2000'] is not None else "NULL",
                    data['Gmag'] if data['Gmag'] is not None else "NULL",
                    data['Plx'] if data['Plx'] is not None else "NULL",
                    data['Teff'] if data['Teff'] is not None else "NULL",
                    data['PM'] if data['PM'] is not None else "NULL",
                    abs_mag if abs_mag is not None else "NULL"
                ])

# Record the end time
end_time = time.time()

# Calculate and print the processing time
process_time = end_time - start_time
print(f"Data saved to {output_file}. Process time: {process_time:.2f} seconds")
