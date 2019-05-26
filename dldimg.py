#!/usr/local/bin/python3

import urllib.request
import urllib.parse
from io import StringIO
from PIL import Image
from math import log, exp, tan, atan, pi, ceil, cos
from geomath import meters2lat, meters2lon, dm2decdeg, dms2decdeg, checkformat
from geomath import convert2decdeg


EARTH_RADIUS = 6378137.0
EQUATOR_CIRCUMFERENCE = 2 * pi * EARTH_RADIUS
INITIAL_RESOLUTION = EQUATOR_CIRCUMFERENCE / 256.0
ORIGIN_SHIFT = EQUATOR_CIRCUMFERENCE / 2.0


def latlontopixels(lat, lon, zoom):
    mx = (lon * ORIGIN_SHIFT) / 180.0
    my = log(tan((90 + lat) * pi / 360.0))/(pi / 180.0)
    my = (my * ORIGIN_SHIFT) / 180.0
    res = INITIAL_RESOLUTION / (2**zoom)
    px = (mx + ORIGIN_SHIFT) / res
    py = (my + ORIGIN_SHIFT) / res
    return px, py


def pixelstolatlon(px, py, zoom):
    res = INITIAL_RESOLUTION / (2**zoom)
    mx = px * res - ORIGIN_SHIFT
    my = py * res - ORIGIN_SHIFT
    lat = (my / ORIGIN_SHIFT) * 180.0
    lat = 180 / pi * (2*atan(exp(lat*pi/180.0)) - pi/2.0)
    lon = (mx / ORIGIN_SHIFT) * 180.0
    return lat, lon


############################################

lat = input('Please enter lat: ').replace(',', '.').split()
lon = input('Please enter lon: ').replace(',', '.').split()
height = int(input('Please enter height [m]: '))
width = int(input('Please enter width [m]: '))
zoom = int(input('Please enter zoom (1-19): '))

lat, lon = convert2decdeg(lat, lon)

upperlat, lowerlat = meters2lat(lat, height)
upperlat, lowerlat = str(upperlat), str(lowerlat)

rightlon, leftlon = meters2lon(lat, lon, width)
rightlon, leftlon = str(rightlon), str(leftlon)

upperleft = upperlat + ',' + leftlon
lowerright = lowerlat + ',' + rightlon

print("Upper left corner: " + upperleft)
print("Lower right corner: " + lowerright)
############################################

ullat, ullon = map(float, upperleft.split(','))
lrlat, lrlon = map(float, lowerright.split(','))

# Set some important parameters
scale = 1
maxsize = 640

# convert all these coordinates to pixels
ulx, uly = latlontopixels(ullat, ullon, zoom)
lrx, lry = latlontopixels(lrlat, lrlon, zoom)

# calculate total pixel dimensions of final image
dx, dy = lrx - ulx, uly - lry

# calculate rows and columns
cols, rows = int(ceil(dx/maxsize)), int(ceil(dy/maxsize))
print("Downloading %d images." % (cols * rows))
# calculate pixel dimensions of each small image
bottom = 120
largura = int(ceil(dx/cols))
altura = int(ceil(dy/rows))
alturaplus = altura + bottom

final = Image.new("RGB", (int(dx), int(dy)))
for x in range(cols):
    for y in range(rows):
        dxn = largura * (0.5 + x)
        dyn = altura * (0.5 + y)
        latn, lonn = pixelstolatlon(ulx + dxn, uly - dyn - bottom/2, zoom)
        position = ','.join((str(latn), str(lonn)))
        print(x, y, position)
        urlparams = urllib.parse.urlencode({'center': position,
                                      'zoom': str(zoom),
                                      'size': '%dx%d' % (largura, alturaplus),
                                      'maptype': 'satellite',
                                      'sensor': 'false',
                                      'scale': scale})
        url = 'http://maps.google.com/maps/api/staticmap?' + urlparams
        print(url)
        f = urllib.request.urlopen(url)
        im = Image.open(StringIO.StringIO(f.read()))
        final.paste(im, (int(x*largura), int(y*altura)))
final.save("tmp-dldimg.png", "PNG")
