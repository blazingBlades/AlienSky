import pandas as pd
import numpy as np
from datetime import datetime

# Try to load the CSV file
try:
    data = pd.read_csv('for_cal.csv', on_bad_lines='skip')
except Exception as e:
    print(f"Error reading the CSV file: {e}")

# Proceed if data was loaded successfully
if 'data' in locals():  # Check if data variable is defined
    # Strip whitespace from column names
    data.columns = data.columns.str.strip()

    # Convert the last updated date to datetime (format: YYYY-MM-DD)
    if 'rowupdate' in data.columns:
        data['last_updated'] = pd.to_datetime(data['rowupdate'])
    else:
        print("The 'rowupdate' column is not found in the DataFrame.")

    # Constants
    G = 6.67430e-11  # gravitational constant in m^3 kg^-1 s^-2
    M_sun = 1.989e30  # mass of the sun in kg

    def calculate_planet_position_and_orientation(row, current_time):
        # Extract parameters
        a = row['pl_orbsmax'] * 1.496e11  # semi-major axis in meters
        P = row['pl_orbper'] * 86400  # orbital period in seconds
        e = row['pl_orbeccen']  # eccentricity
        i = row['pl_orbincl'] * np.pi / 180  # inclination in radians
        M_star = row['st_mass'] * M_sun  # mass of the star in kg
        
        # Check for NaN values before calculations
        if any(pd.isna([a, P, e, i, M_star])):
            return None, None  # Return None for both position and orientation

        # Mean motion
        n = np.sqrt(G * M_star / a**3)

        # Calculate elapsed time since last update
        elapsed_time = (current_time - row['last_updated']).total_seconds()
        
        # Mean anomaly
        M = n * elapsed_time  # Mean anomaly in radians

        # Solve Kepler's equation for E
        E = M  # Initial guess
        for _ in range(10):  # Iterate to solve for E
            E = M + e * np.sin(E)

        # Calculate true anomaly
        nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))

        # Calculate position in 2D
        x = a * (np.cos(E) - e)
        y = a * np.sqrt(1 - e**2) * np.sin(E)

        # Convert to 3D
        Omega = 0  # Longitude of ascending node (radians)
        omega = 0  # Argument of periapsis (radians)
        
        # Apply rotation
        x_orb = x
        y_orb = y * np.cos(i)  # Simplified for demonstration
        z_orb = y * np.sin(i)

        # Final position with respect to the host star
        position = (x_orb, y_orb, z_orb)

        # Orientation (true anomaly and inclination)
        orientation = (nu, i)  # You can choose to return other orientation parameters

        return position, orientation  # Return both position and orientation

    # Get the current time
    current_time = datetime.now()

    # Prepare a list to hold the results
    results = []

    # Calculate position and orientation for planets
    for index, planet in data.iterrows():
        position, orientation = calculate_planet_position_and_orientation(planet, current_time)
        
        if position:
            results.append({
                'pl_name': planet['pl_name'],
                'hostname': planet['hostname'],
                'hip': planet['hip_name'],
                'x': position[0],
                'y': position[1],
                'z': position[2],
                'true_anomaly': orientation[0],  # True anomaly
                'inclination': orientation[1],    # Inclination
                'last_updated': planet['last_updated']
            })

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results)

    # Output to a CSV file
    output_file = 'planet_positions.csv'
    results_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
