import requests

def get_exoplanet_data():
    # NASA Exoplanet Archive API URL
    exoplanet_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=SELECT%20planet_name,%20host_star_name,%20pl_radius%20FROM%20exoplanets%20WHERE%20planet_name='Kepler-22b'"
    
    # Making the API request
    response = requests.get(exoplanet_url)
    
    # Checking for a successful response
    if response.status_code == 200:
        # Print the JSON response for debugging
        print(response.json())
        return response.json()
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
        # Only get the first entry (Kepler-22b)
        planet = exoplanet_data[0]
        planet_name = planet['planet_name']
        star_name = planet['host_star_name']
        radius = planet['pl_radius']
        
        # Getting star position
        star_position = get_star_position(star_name)
        
        print(f"Planet: {planet_name}, Host Star: {star_name}, Radius: {radius}, Star Position:\n{star_position}\n")

if __name__ == "__main__":
    main()
