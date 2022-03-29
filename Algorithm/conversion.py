

# Import library
from  pyproj import Proj
from shapely.ops import transform
from shapely.geometry import Point
from functools import partial


 # London Heathrow Airport - Airspace coordinates bound
lat1, lon1 = 51.65, 0.15
lat2, lon2 = 51.25, -0.85

lat3, lon3 = 51.65, -0.85
lat4, lon4 = 51.25, 0.15


# LTMA - Bound within LTMA-11 A
lat5, lon5 = 51.48, -0.605

# LTMA - Bound within LTMA-4 A
lat6, lon6 = 51.27, -0.73
lat7, lon7 = 51.29, -0.68
lat8, lon8 = 51.29, -0.62
lat9, lon9 = 51.27, -0.64
lat10, lon10 = 51.26, -0.67
lat11, lon11 = 51.27, -0.69



# Convert the lon/lat coordinates to Eastings/Northings
top = Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
x1 = top(lon1, lat1)

left = Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
x2 = left(lon3, lat3)

bottom = Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
y1 = bottom(lon2, lat2)

right = Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
y2 = right(lon4, lat4)


# Inner Boundaries - Polygons and Circle 
# Perform conversion as previous for each restricted area

# For a circle bound - R104/2.4
km = 10
proj_wgs84 = Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +zone=30 +epsg=2395')
aeqd_proj = f'+proj=aeqd +lat_0={lat5} +lon_0={lon5}'
projection = partial(transform, Proj(aeqd_proj.format(lat=lat5, lon=lon5)), proj_wgs84)
ltma_bound = Point(0, 0).buffer(km * 1000).boundary  # distance in metres

#print(ltma_bound)


# Coordinates for a Polygon bound - D132/2.5

top = Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
a1 = top(lon6, lat6)

left = Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
a2 = left(lon7, lat7)

bottom = Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
b1 = bottom(lon8, lat8)

right = Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
b2 = right(lon9, lat9)

bottom = Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
c1 = bottom(lon10, lat10)

right = Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
c2 = right(lon11, lat11)