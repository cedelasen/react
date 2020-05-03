#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#José María de la Sen Molina, @cedelasen

import dcel as dc
from scipy.spatial import Voronoi, voronoi_plot_2d
import plottingModule as pM
import finiteVor as fV


def dcelInstance(vL, eL, maxX, maxY, xRange, yRange):

    fixX = xRange/maxX
    fixY = yRange/maxY

    for v in vL:
        v[0] = fixX*v[0]
        v[1] = fixY*v[1]

    d = dc.Dcel(vL, eL)
    d.build_dcel()

    return d


def generatorPointsToDcelInstance(gL, minX, maxX, minY, maxY, rangeX, rangeY):
    
    vor = Voronoi(gL)
    #voronoi_plot_2d(vor)           
    #pM.plt.show()
    
    polygons = fV.vorFiniteDelPolygonsList(vor, minX, maxX, minY, maxY)
    
    file = open("generatorPointsToDcel.txt","w") 
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

    return dcelInstance(vertices, edges, maxX, maxY, rangeX, rangeY)
