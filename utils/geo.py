
from math import radians, sin, cos, sqrt, atan2
def haversine(lat1, lon1, lat2, lon2):
    R=6371.0; dlat=radians(lat2-lat1); dlon=radians(lon2-lon1)
    a=sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2*R*atan2(sqrt(a), sqrt(1-a))
def nearest(lat, lon, items):
    best=None; best_d=10**9
    for it in items:
        d=haversine(lat,lon,it[2],it[3])
        if d<best_d: best_d, best=d, it
    return best, best_d
