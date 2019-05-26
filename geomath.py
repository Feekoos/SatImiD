from math import cos, pi


EARTH_RADIUS = 6378137.0
EQUATOR_CIRCUMFERENCE = 2 * pi * EARTH_RADIUS
INITIAL_RESOLUTION = EQUATOR_CIRCUMFERENCE / 256.0
ORIGIN_SHIFT = EQUATOR_CIRCUMFERENCE / 2.0


def meters2lat(lat, meters):
    dlat = (meters / 2) / EARTH_RADIUS
    return lat + (dlat * (180 / pi)), lat - (dlat * (180 / pi))


def meters2lon(lat, lon, meters):
    dlon = (meters / 2) / (EARTH_RADIUS * cos(pi * lat / 180))
    return lon + (dlon * (180 / pi)), lon - (dlon * (180 / pi))


def dm2decdeg(dm):
    d = float(dm[0])
    m = float(dm[1])
    d = d + (m / 60)
    return d


def dms2decdeg(dms):
    d = float(dms[0])
    m = float(dms[1])
    s = float(dms[2])
    m = m + (s / 60)
    d = d + (m / 60)
    return d


def checkformat(x):
    if len(x) == 3:
        return 'dms'
    if len(x) == 2:
        return 'dm'
    if len(x) == 1:
        return 'd'


def convert2decdeg(lat, lon):

    # Lattitude
    if checkformat(lat) == 'd':
        retlat = float(lat[0])
    if checkformat(lat) == 'dm':
        retlat = dm2decdeg(lat)
    if checkformat(lat) == 'dms':
        retlat = dms2decdeg(lat)

    # Lattitude
    if checkformat(lon) == 'd':
        retlon = float(lon[0])
    if checkformat(lon) == 'dm':
        retlon = dm2decdeg(lon)
    if checkformat(lon) == 'dms':
        retlon = dms2decdeg(lon)

    return retlat, retlon
