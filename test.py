from astroquery.vizier import Vizier

# Set a limit for the number of rows you want to fetch (adjust as needed)
Vizier.ROW_LIMIT = 1811709771

# Define the Gaia DR3 catalog and HIP ID you want to query
catalog = "I/355/gaiadr3"  # Gaia DR3 catalog
hip_id = 1  # Replace with the desired HIP ID

# Query Vizier using HIP ID constraint
result = Vizier.query_constraints(catalog=catalog, HIP=str(hip_id))

# Check and display the result
if result:
    gaia_dr3_data = result[0]
    print(gaia_dr3_data)
else:
    print("No data found for HIP ID:", hip_id)
