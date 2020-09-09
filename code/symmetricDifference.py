"""
@author: cedelasen
"""
from shapely.geometry import (
    Polygon,
    Point
)

def localSymDif(face, polygons, box):
    
    """ returns the symmetric difference between a dcel's face and his correspondent polygon of the list of voronoi's polygon (index by shared point) """
    
    p = face.point #get the point to 'index' in polygons list
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


def symDif(faces, polygons, box): #faces and polygons list as parameter
    
    """ returns the global symmetric difference between the dcel and the list of voronoi's polygons """
    
    dS = 0
    for f in faces:
        dS = dS + localSymDif(f, polygons, box)
    return (dS/2)/box.area
             


def symDifPeer(face1, face2, polygons, box):
    
    max_X = box.bounds[2]
    max_Y = box.bounds[3]
    dS = (localSymDif(face1, polygons, box) + localSymDif(face2, polygons, box))/2
    total = max_X*max_Y
    return dS/total



def symDifGroup(faces, polygons, box):
    
    dS = 0
    max_X = box.bounds[2]
    max_Y = box.bounds[3]
    for f in faces:
        dS = dS + localSymDif(f, polygons, box)
    dS = dS/2
    total = max_X*max_Y
    return dS/total
    


def symDifColours(faces, polygons, colour, box):
    
    dS = 0
    max_X = box.bounds[2]
    max_Y = box.bounds[3]
    for f in faces:
        if f.color == colour:
            dS = dS + localSymDif(f, polygons, box)
    dS = dS/2
    total = max_X*max_Y
    return dS/total



def andChainColours(faces, polygonsOld, polygonsNew, colour, box):
    
    res = True
    for f in faces:
        if f.color == colour:
            msdOld = localSymDif(f, polygonsOld, box)
            msdNew = localSymDif(f, polygonsNew, box)
            comp = (msdNew <= msdOld)
            res = res and comp
    return res



def orChainColours(faces, polygonsOld, polygonsNew, colour, box):
    
    res = False
    for f in faces:
        if f.color == colour:
            msdOld = localSymDif(f, polygonsOld, box)
            msdNew = localSymDif(f, polygonsNew, box)
            comp = (msdNew <= msdOld)
            res = res or comp
    return res



def numbersColours(faces, polygonsOld, polygonsNew, colour, box):
    
    better = 0 
    worse = 0
    for f in faces:
        if f.color == colour:
            msdOld = localSymDif(f, polygonsOld, box)
            msdNew = localSymDif(f, polygonsNew, box)
            comp = (msdNew <= msdOld)
            if comp:
                better += 1
            else:
                worse += 1
    return better, worse
