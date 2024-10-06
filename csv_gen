from astroquery.vizier import Vizier
import csv

# Set a limit for the number of rows you want to fetch (adjust as needed)
Vizier.ROW_LIMIT = 1_811_709_771

# Define the Gaia DR3 catalog
catalog = "I/355/gaiadr3"  # Gaia DR3 catalog

# File to save the output
output_file = "gaia_dr3_hip_ids.csv"

# Open the CSV file for writing
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["HIP ID", "Gaia DR3 Data"])
    
    # Loop over HIP IDs from 1 to 118,218
    for hip_id in range(1, 118219):
        # Query Vizier using HIP ID constraint
        result = Vizier.query_constraints(catalog=catalog, HIP=str(hip_id))
        
        # Check if data is found, otherwise write "Null"
        if result:
            gaia_dr3_data = result[0]
            writer.writerow([hip_id, gaia_dr3_data])
        else:
            writer.writerow([hip_id, "Null"])
        
        # Optional: Print progress
        if hip_id % 1000 == 0:
            print(f"Processed HIP ID {hip_id}")

print(f"Data saved to {output_file}")
