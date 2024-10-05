from astroquery.vizier import Vizier

# Define the HIP number
hip_number = 122

# Query the Hipparcos catalog for the specified HIP number
result = Vizier.query_constraints(catalog='I/239/hip_main', HIP=hip_number)

# Check if we got any results
if result and len(result) > 0:
    star_data = result[0]
    # Print the columns available in the retrieved data
    print("Available columns:", star_data.columns)
    
    # Attempt to fetch the B-V color index
    if 'B-V' in star_data.columns:
        b_v_color = star_data['B-V'][0]  # Get the first entry for the B-V color index
        print(f"B-V Color Index for HIP {hip_number}: {b_v_color}")
    else:
        print("B-V color index not found.")
else:
    print(f"No data found for HIP {hip_number}.")
