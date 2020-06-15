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


def dcelInstanceByGeneratorPoints(gL, iniX, finX, iniY, finY, rangeX, rangeY):
    
    vor = Voronoi(gL)
    
    polygons = finiteVoronoi.vorFiniteDelPolygonsList(vor, iniX, finX, iniY, finY)
    
    file = open("tmp/generatorPointsToDcel.txt","w") 
    file.flush
    
    aux_vertices = []
    
    for p in polygons:
        cL = p.exterior.coords
        for c in cL:
            aux_vertices.append([c[0],c[1]])
    
    vertices =  []       
    cont = 0
    
    for v in aux_vertices:
        if v not in vertices:
            vertices.append(v)
            file.write("Vert num: " + str(cont) + "   " + str(v) + "\n")
            cont += 1
            
    edges =  []       
    cont = 0
    
    file.write("\n\n\n\n")
    
    for p in polygons: 
        cL = p.exterior.coords
        file.write("Polygon number: " + str(cont) + "\n")
        file.write("------------------ Coords: \n")
        for c in cL:
            file.write(str(c) + "\n")
        file.write("------------------ Edges: \n")
        n = len(cL)
        for i in range(0, n-1):
            pos1 = vertices.index([cL[i][0],cL[i][1]])
            pos2 = vertices.index([cL[i+1][0], cL[i+1][1]])       
            edge = [pos1, pos2]
            file.write(str(edge)+ "\n")  
            edge.sort()
            if edge not in edges:
                edges.append(edge) 
                #(edge)
        cont += 1
        file.write("\n\n")
     
    file.close

    return dcelInstance(vertices, edges, iniX, finX, iniY, finY, rangeX, rangeY)
