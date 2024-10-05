from skyfield.api import load
from skyfield.data import hipparcos

# Load the Hipparcos data
with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)

# Filter the DataFrame to keep only rows with non-null RA (Right Ascension) values
df = df[df['ra_degrees'].notnull()]
filtered_df = df[df['magnitude'] <= 5] # brightness filtering #6 beacuse it is naked eye limit

# Now you can display or work with your filtered DataFrame
filtered_df.to_csv('hip_data_l6.csv', index=True)

#print(filtered_df)

# If you want to avoid keeping the large DataFrame, you can also delete it
del df
