from astroquery.vizier import Vizier
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set the catalog and file output
catalog = "I/355/gaiadr3"  # Gaia DR3 catalog
output_file = "gaia_batch.csv"

# Function to query the database
def query_hip(hip_id):
    # Specify only the columns you need (e.g., RAJ2000, DEJ2000, Gmag)
    result = Vizier.query_constraints(catalog=catalog, HIP=str(hip_id), columns=['RAJ2000', 'DEJ2000', 'Gmag'])
    if result:
        # Check if result[0] has multiple rows and take the first one
        data = result[0]
        if len(data) > 0:
            return hip_id, data[0]  # Return HIP ID and the first row of data
    return hip_id, "Null"  # Return HIP ID and "Null" if no data is found

# Open the CSV file for writing
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["HIP ID", "RAJ2000", "DEJ2000", "Gmag"])  # Write header with specific columns

    # Use ThreadPoolExecutor to parallelize the queries
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        futures = []

        # Loop over HIP IDs in range
        for hip_id in range(1, 20):  # Adjust to the desired range ##118219
            futures.append(executor.submit(query_hip, hip_id))  # Submit each HIP ID for querying

        for future in as_completed(futures):
            hip_id, data = future.result()
            if isinstance(data, str):  # Check if data is "Null"
                writer.writerow([hip_id, "Null"])  # Write HIP ID with "Null"
            else:
                # Write HIP ID and relevant data, ensure data is accessed correctly
                writer.writerow([hip_id, data['RAJ2000'], data['DEJ2000'], data['Gmag']])

print(f"Data saved to {output_file}")
