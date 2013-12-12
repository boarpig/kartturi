#!/usr/bin/python

from PIL import Image, ImageChops
from math import ceil, fabs
from urllib import urlretrieve
from optparse import OptionParser

def horzAdd(left, right):
    if left.size[1] == right.size[1]:
        w, h = (left.size[0] + right.size[0])-120, left.size[1]
        outimg = Image.new('RGB', (w, h))
        left = left.crop((0, 0, left.size[0]-60, left.size[1]))
        right = right.crop((60, 0, right.size[0], right.size[1]))
        left.load()
        right.load()
        outimg.paste(left, (0,0))
        outimg.paste(right, (left.size[0],0))
        return outimg

def vertAdd(upper, lower):
    if upper.size[0] == lower.size[0]:
        w, h = upper.size[0], (upper.size[1] +lower.size[1])-120
        outimg = Image.new('RGB', (w, h))
        upper = upper.crop((0, 0, upper.size[0], upper.size[1]-60))
        lower = lower.crop((0, 60, lower.size[0], lower.size[1]))
        upper.load()
        lower.load()
        outimg.paste(upper, (0,0))
        outimg.paste(lower, (0, upper.size[1]))
        return outimg

def getMap(coord):
    coordstr = str(coord[0]) + ',' + str(coord[1]) + ',' + str((coord[0])+2400) + ',' + str((coord[1])+2400)
    mapname = ''
    url = "http://kansalaisen.karttapaikka.fi/image?" + "request=GetMap" + \
        "&bbox=" + coordstr + "&scale=80000" + "&width=600" + \
        "&height=600" + "&srs=EPSG:3067" + "&styles=normal" + \
        "&lang=fi" + "&lmid=1386864555392" #"&lmid=1210782329134"
    mapname, header = urlretrieve(url)
    print(url)
    outimg = Image.open(mapname)
    return outimg

def genMap(coords=(0,0,0,0)):
    coords = list(coords)
    for i, value in enumerate(coords):
        coords[i] = value*1000
    addition = 1920
    width = int(fabs(ceil((coords[2]-coords[0])/float(addition))))
    height = int(fabs(ceil((coords[3]-coords[1])/float(addition))))
    maara = width *(height+2)
    monesko = 0
    for x in xrange(width):
        for y in xrange(height+2):
            monesko += 1
            print("%.0f%%, %i/%i" % (monesko/float(maara)*100, monesko, maara))
            coord = (coords[0] + x*addition, coords[1] - y*addition)
            if y == 0:
                column = getMap(coord)
            else:
                newmap = getMap(coord)
                column = vertAdd(column, newmap)
        if x == 0:
            whole = column.copy()
        else:
            whole = horzAdd(whole, column)
    whole.save('koko.png')

def main():
    pass

if __name__ == "__main__":
    main()

genMap((425,7205,431,7199))
