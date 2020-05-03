"""
@author: cedelasen
"""

from shapely.geometry import Polygon, Point
import plottingModule as pM

def miniSymDif(face, polygons, box):
    
    """ returns the symmetric difference between a dcel's face and his correspondent polygon of the list of voronoi's polygon (index by shared point) """
    
    p = face.point       #get the point to 'index' in polygons list
    found = False
    cont = 0
    while not found:
        poly = polygons[cont] 
        if poly.contains(Point(p[0],p[1])):
            polyFace = Polygon(face.coordsList())
            polySelected = polygons[cont]
            polySelected = polySelected.intersection(box)
            dS = polyFace.symmetric_difference(polySelected).area
            found = True
        else:
            cont += 1
    return dS

def symDif(dcel, polygons, box):     #dcel and polygons list as parameter
    
    """ returns the global symmetric difference between the dcel and the list of voronoi's polygons """
    
    dS = 0
    for f in dcel.faces:
        dS = dS + miniSymDif(f, polygons, box)
    return (dS/2)/box.area
             

def symDifPeer(face1, face2, polygons, box, max_X, max_Y):
    
    dS = (miniSymDif(face1, polygons, box) + miniSymDif(face2, polygons, box))/2
    total = max_X*max_Y
    return dS/total

def symDifGroup(faces, polygons, box, max_X, max_Y):
    
    dS = 0
    for f in faces:
        dS = dS + miniSymDif(f, polygons, box)
    dS = dS/2
    total = max_X*max_Y
    return dS/total
    

def symDifColours(faces, polygons, colour, box, max_X, max_Y):
    
    dS = 0
    for f in faces:
        if f.color == colour:
            dS = dS + miniSymDif(f, polygons, box)
    dS = dS/2
    total = max_X*max_Y
    return dS/total


def andChainColours(faces, polygonsOld, polygonsNew, colour, box):
    
    res = True
    for f in faces:
        if f.color == colour:
            msdOld = miniSymDif(f, polygonsOld, box)
            msdNew = miniSymDif(f, polygonsNew, box)
            comp = (msdNew <= msdOld)
            res = res and comp
    return res


def orChainColours(faces, polygonsOld, polygonsNew, colour, box):
    
    res = False
    for f in faces:
        if f.color == colour:
            msdOld = miniSymDif(f, polygonsOld, box)
            msdNew = miniSymDif(f, polygonsNew, box)
            comp = (msdNew <= msdOld)
            res = res or comp
    return res


def numbersColours(faces, polygonsOld, polygonsNew, colour, box):
    
    better = 0 
    worse = 0
    for f in faces:
        if f.color == colour:
            msdOld = miniSymDif(f, polygonsOld, box)
            msdNew = miniSymDif(f, polygonsNew, box)
            comp = (msdNew <= msdOld)
            if comp:
                better += 1
            else:
                worse += 1
    return better, worse
