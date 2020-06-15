"""
@author: cedelasen
"""

import numpy
import math
import time 
from sympy.geometry import (
    Line
)
from shapely.geometry import ( 
    Point
)

def sumatorio(vector):
    sum = 0
    for i in vector:
        sum += i
    return sum


def generateRandomPoint(polygon):
    
    """ returns a random point inside a polygon
    
    source : https://gis.stackexchange.com/questions/207731/how-to-generate-random-coordinates-in-a-multipolygon-in-python
    
    state : modified
    
    """
    
    numpy.random.seed(int(time.time()))
    minx, miny, maxx, maxy = polygon.bounds
    pnt = Point([numpy.random.uniform(minx, maxx), numpy.random.uniform(miny, maxy)])

    while not polygon.contains(pnt):
        pnt = Point([numpy.random.uniform(minx, maxx), numpy.random.uniform(miny, maxy)])

    return [pnt.x, pnt.y]


def mod2Points(p1,p2):
    
    """ returns vector's module operation """
    
    return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)


def disturbPoint(point, polygon):
    
    """ disturbs a point (inside a polygon). """ 
    
    inside = False
    d = 0.3 #dmax
    cL = polygon.exterior.coords
    for c in cL:
        aux = mod2Points(point,c)
        if aux > d:
            d = aux
    while(not inside):
        zeta = numpy.random.uniform(0,2*math.pi)      #generate random value 0-2pi
        l = numpy.random.uniform(0, d)             #generate random value 0-d(the shortest distance between a point and a face's vertex)
        nP = [point[0] + l*math.cos(zeta), point[1] + l*math.sin(zeta)]
        inside = polygon.contains(Point(nP[0],nP[1]))
        
    return  [point[0] + l*math.cos(zeta), point[1] + l*math.sin(zeta)]


def simmetricPoint(p, p1, p2):
    
    """ returns the simmetric of point respect a line (p1-p2) """
    
    l1 = Line(p1, p2)
    l2 = l1.perpendicular_line(p)
    point = l2.intersection(l1)
    x = point[0][0]*2-p[0]
    y = point[0][1]*2-p[1]
    return [x,y]


def indexByPoint(point, polygons):
    
    """ index polygon's list by point """
    
    cont = 0
    found = False
    
    poly = None
    
    while(not found):
        poly = polygons[cont]
        if (poly.contains(Point(point[0], point[1]))):
            found = True
        else:
            cont += 1
        
    return poly
    

def isValid(face, iniX, finX, iniY, finY):
    
    """ returns true if the face passed as parameter is not external """
    
    p1 = [iniX, iniY]
    p2 = [iniX, finY]
    p3 = [finX, iniY]
    p4 = [finX, finY]
    
    points = [p1,p2,p3,p4]
    
    cont = 0
    
    coords = face.coordsList()
    
    for p in points:
        cont += coords.count(p)
    
    return cont<3
