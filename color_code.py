import pandas as pd
from astroquery.vizier import Vizier

# Load your CSV file
df = pd.read_csv('ra_de_data.csv')

def fetch_star_colors_batch(hip_numbers):
    color_dict = {}  # Dictionary to store colors for each HIP number
    # Process in batches of 100
    for i in range(0, len(hip_numbers), 100):
        batch = hip_numbers[i:i + 100]  # Get a batch of 100 HIP numbers
        try:
            # Convert HIP numbers to strings to avoid type issues
            batch_str = [str(int(hip)) for hip in batch]
            
            # Query multiple HIP numbers at once
            results = Vizier.query_constraints(catalog='I/239/hip_main', HIP=batch_str)
            if results and len(results) > 0:
                star_data = results[0]  # This should be a Table object
                
                # Check if 'B-V' exists in the columns
                if 'B-V' in star_data.colnames:
                    for row in star_data:
                        hip_number = row['HIP']  # Get the HIP number
                        b_v_color = row['B-V']  # Get B-V color index
                        
                        # Store the color in the dictionary only if it exists
                        if b_v_color is not None:
                            color_dict[hip_number] = b_v_color
                else:
                    print(f"B-V color index not found in batch starting with HIP {batch[0]}.")
            else:
                print(f"No data found for batch starting with HIP {batch[0]}.")
        except Exception as e:
            print(f"Error fetching data for batch starting with HIP {batch[0]}: {e}")
    
    return color_dict

# Get unique HIP numbers from the DataFrame
hip_numbers = df['Star HIP'].unique()

# Fetch colors in batches
color_dict = fetch_star_colors_batch(hip_numbers)

# Create a DataFrame from the color dictionary
color_df = pd.DataFrame(list(color_dict.items()), columns=['Star HIP', 'Color'])

# Save the DataFrame to a new CSV
color_df.to_csv('hip_color.csv', index=False)
print("Updated CSV file with star colors saved as 'hip_color.csv'.")
