from skyfield.api import Star, load
from skyfield.data import hipparcos

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)
df = df[df['ra_degrees'].notnull()]## dataframe filtering


tar_star = Star.from_dataframe(df.loc[87937])

planets = load('de421.bsp')
sun = planets['sun']

ts = load.timescale()
t = ts.now()
#t = ts.utc(2010, 9, 3) for exact time
astrometric = sun.at(t).observe(tar_star)
ra, dec, distance = astrometric.radec()
print(ra)
print(dec)
print(distance)

df = df[df['magnitude'] <= 5] # brightness filtering #6 beacuse it is naked eye limit
print('After filtering, there are {} stars'.format(len(df)))
