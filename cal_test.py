import requests
import pandas as pd
from io import StringIO

def get_exoplanet_data():
    # NASA Exoplanet Archive API URL
    exoplanet_url = (
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
        "query=SELECT+pl_name,hostname,pl_rade+FROM+ps+WHERE+pl_name='Kepler-22%20b'&format=csv"
    )
    
    # Making the API request
    response = requests.get(exoplanet_url)
    
    # Checking for a successful response
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching exoplanet data: {response.status_code} - {response.text}")
        return None

def calculate_planet_position(star_name, planet_name):
    # Placeholder logic for real-time position calculation
    # Replace with actual logic as needed
    return f"Real-time position of {planet_name} from {star_name}"

def main():
    exoplanet_data = get_exoplanet_data()
    
    if exoplanet_data:
        # Use pandas to read the CSV-like response
        df = pd.read_csv(StringIO(exoplanet_data))
        
        # Remove duplicates based on pl_name and hostname
        df_unique = df.drop_duplicates(subset=['pl_name', 'hostname']).reset_index(drop=True)

        for index, planet in df_unique.iterrows():
            planet_name = planet['pl_name']
            star_name = planet['hostname']
            
            # Calculate the real-time position of the planet from its host star
            position = calculate_planet_position(star_name, planet_name)
            
            print(f"Planet: {planet_name}, Host Star: {star_name}, Position: {position}\n")

if __name__ == "__main__":
    main()
