import pandas as pd

# Function to read CSV, skip the first 38 lines, and create a new DataFrame
def create_new_dataframe(file_path):
    try:
        # Read the CSV file into a DataFrame, skipping the first 38 rows
        df = pd.read_csv(file_path, skiprows=range(0, 38), on_bad_lines='skip')  # Skip lines 1 to 38
        
        return df  # Return the DataFrame
    
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
    except FileNotFoundError:
        print(f"The file was not found: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Set the file path to your CSV
file_path = '/Users/linlekzaw/Desktop/AlienSky/pl_data.csv'  # Replace with your CSV file path

# Create new DataFrame
original_df = create_new_dataframe(file_path)

# Check if the DataFrame is created successfully
if original_df is not None:
    # Ensure 'rowupdate' is in datetime format
    original_df['rowupdate'] = pd.to_datetime(original_df['rowupdate'], errors='coerce')

    # Remove duplicates, keeping the latest row for each pl_name
    latest_rows = original_df.loc[original_df.groupby('pl_name')['rowupdate'].idxmax()]

    # Reset the index of the new DataFrame
    latest_rows.reset_index(drop=True, inplace=True)

    # Display the resulting DataFrame
    print("DataFrame with duplicates removed, keeping the latest row:")
    print(latest_rows)

    # Optionally, display the shape of the new DataFrame
    print(f"\nNew DataFrame shape: {latest_rows.shape}")
  # Set the file path where you want to save the new DataFrame
output_file_path = '/Users/linlekzaw/Desktop/AlienSky/processed_pl_data.csv'  # Change the path as needed

# Save new_df to CSV
original_df.to_csv(output_file_path, index=False)
