import requests
import pandas as pd
from io import StringIO

def get_exoplanet_data():
    # NASA Exoplanet Archive API URL for the specific exoplanet
    exoplanet_url = (
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
        "query=SELECT+pl_name,hostname,pl_rade+FROM+ps+WHERE+pl_name='Kepler-22%20b'&format=csv"
    )
    
    # Making the API request
    response = requests.get(exoplanet_url)
    
    # Checking for a successful response
    if response.status_code == 200:
        print("Response content:", response.text)  # For debugging
        return response.text
    else:
        print(f"Error fetching exoplanet data: {response.status_code} - {response.text}")
        return None

def get_star_position(star_name):
    # SIMBAD API URL for querying the host star
    simbad_url = f"http://simbad.u-strasbg.fr/simbad/sim-id?Ident={star_name}&output.format=3"
    
    # Making the API request
    response = requests.get(simbad_url)
    
    # Checking for a successful response
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching position for {star_name}.")
        return None

def main():
    exoplanet_data = get_exoplanet_data()
    
    if exoplanet_data:
        # Use pandas to read the CSV-like response and remove duplicates
        df = pd.read_csv(StringIO(exoplanet_data))
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        for index, planet in df.iterrows():
            planet_name = planet['pl_name']
            star_name = planet['hostname']
            radius = planet['pl_rade'] if pd.notnull(planet['pl_rade']) else "Unknown"
            
            # Getting star position
            star_position = get_star_position(star_name)
            
            print(f"Planet: {planet_name}, Host Star: {star_name}, Radius: {radius}, Star Position:\n{star_position}\n")

if __name__ == "__main__":
    main()
