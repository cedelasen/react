"""
@author: cedelasen
"""

import dcel
import finiteVoronoi
from scipy.spatial import (
    Voronoi
)
from shapely.geometry import (
    Polygon
)

def dcelInstanceByVerticesEdges(vL, eL, iniX, finX, iniY, finY, rangeX, rangeY):

    maxX = rangeX/finX
    maxY = rangeY/finY

    for v in vL:
        v[0] = maxX*v[0]
        v[1] = maxY*v[1]

    box = Polygon([[iniX, iniY], [iniX, rangeY], [rangeX, rangeY], [rangeX, iniY]])
    d = dcel.Dcel(vL, eL, box)
    d.build_dcel()

    return d
