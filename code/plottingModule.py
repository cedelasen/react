"""
@author: cedelasen
"""

import numpy
import matplotlib.pyplot as plt
from scipy.spatial import (
    ConvexHull,
)


def plotPoints(points, color):
    
    """ plot points with the color passed as parameter"""
    
    for p in points:
        plt.plot(p[0], p[1], color)


def plotPoly(poly, color): #shapely.geometry.Polygon
    
    """ plot poly with the color passed as parameter """
    
    plotConvexHull(poly.exterior.coords, color)


def plotPolys(polys, color):
    
    """ plot polys with the color passed as parameter"""

    for p in polys:
        plotPoly(p, color)


def plotConvexHull(vList, color):#ndarray
    
    """ vertices list -> Plot polygon (convex hull) with the color passed as parameter """
    
    npArray = numpy.array(vList)
    hull = ConvexHull(npArray)
    for simplex in hull.simplices:
        plt.plot(npArray[simplex, 0], npArray[simplex, 1], color)


def plotDcel(dcel, color):#dcel
    
    """ plot Dcel with the color passed as parameter """
    
    for f in dcel.faces:
        vList = []
        for v in f.vertexList():
            vList.append([v.x,v.y])
        plotConvexHull(vList, color)
    