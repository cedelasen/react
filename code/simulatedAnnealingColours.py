#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#José María de la Sen Molina, @cedelasen

from scipy.spatial import Voronoi
import math as m
import plantingSeeds as pS
import numpy as np
import toolsModule as tM
import finiteVor as fV
import symDif as sDif
import random


def simulatedAnnealingColours_AndMethod(dcel, pointsSet, vorDiagram, polygonsList, sDini, ratio, tInicial, tFinal, l, n, minRandom, maxRandom, box, mode, static):
         
    file = open("sA_colours_and.txt","w") 
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING COLOURS AND METHOD")
    
    pSet = pointsSet                                                             
    vor = vorDiagram                                                            
    polygons = polygonsList                                                     
    sD = sDini                                                                 
    
    bestSD = sD
    bestSet = pSet                                                              #best set of points solution
     
    cont = 0
    t = tInicial                                                                #|negative|
    r = ratio                                                                   # + m.log10(n)
    
    pS.distroPoints(dcel, mode, box.bounds[2], box.bounds[3])
    
    file.write("Number of generating points: " + str(len(pSet))+'\n')
    file.write("Number of faces: " + str(n)+'\n')
    
    while(t>tFinal):
        file.write("Temperatura del sistema: " + str(t)+'\n')
        file.write("Iteracion: " + str(cont)+'\n')
        cont = cont + 1
        it = (t/l)*n #L
        file.write("--- Total subiteraciones NR: " + str(it)+'\n')
        it = int(round(it))+1                                                   #para los casos en los que obtengo 0
        file.write("--- Total subiteraciones R: " + str(it)+'\n')
        
        for i in range (0,it):
            f = dcel.faces[random.randint(0,n-1)]                               #select random face
            color = f.color
            oldPolygons = fV.vorFinitePolygonsList(vor)                         #not delimited
            oldSD = sDif.symDifColours(dcel.faces, oldPolygons, color, box, box.bounds[2], box.bounds[3])
            newPoint = tM.disturbPoint(f.point, f.polygon)           #calculate new point
            file.write("------ Subiteracion num: " + str(i)+'\n')
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point                                                 #save old point
            f.point = newPoint                                                  #change old -> new
            pSet = dcel.points()                                                #rescue all points with new point
            vor = Voronoi(pSet)                                                 #recalculate voronoi
            newPolygons = fV.vorFinitePolygonsList(vor)                         #not delimited
            newSD = sDif.symDifColours(dcel.faces, newPolygons, color, box, box.bounds[2], box.bounds[3])
            
            comp = sDif.andChainColours(dcel.faces, oldPolygons, newPolygons, color, box)
            
            if comp: #and chain
                file.write("Energia local mejorada con nuevo punto : " + str(newPoint)+'\n')
            else:
                delta = newSD - oldSD
                prob = m.e**(-delta/t)
                rand = np.random.uniform(minRandom, maxRandom)
                if(rand > prob):
                    file.write("Energia local no mejorada pero aceptada "+'\n')
                else:
                    file.write("Energia local no mejorada, tampoco aceptada "+'\n')
                    f.point = savePoint
                    pSet = dcel.points()
                    vor = Voronoi(pSet)
                    
            sD = sDif.symDif(dcel, polygons, box)
            if (sD < bestSD):                                               #if best solution
                bestSD = sD                                                 #best symmetric difference <- actual symmetric difference
                bestSet = pSet                                              #best set of generator points <- actual set of generator points
            
            if (not static):
                pS.distroPoints(dcel, mode, box.bounds[2], box.bounds[3])
            
        t = t*r
    file.close
    
    #last it
    polygons = fV.vorFinitePolygonsList(vor)
    pSet = dcel.points()
    sD =  sDif.symDif(dcel, polygons, box)
    
    return bestSet, bestSD, pSet, sD 




def simulatedAnnealingColours_OrMethod(dcel, pointsSet, vorDiagram, polygonsList, sDini, ratio, tInicial, tFinal, l, n, minRandom, maxRandom, box, mode, static):
         
    file = open("sA_colours_or.txt","w") 
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING COLOURS OR METHOD")
    
    pSet = pointsSet                                                             
    vor = vorDiagram                                                            
    polygons = polygonsList                                                     
    sD = sDini                                                                 
    
    bestSD = sD
    bestSet = pSet                                                              #best set of points solution
     
    cont = 0
    t = tInicial                                                                #|negative|
    r = ratio                                                                   # + m.log10(n)
    
    pS.distroPoints(dcel, mode, box.bounds[2], box.bounds[3])
    
    file.write("Number of generating points: " + str(len(pSet))+'\n')
    file.write("Number of faces: " + str(n)+'\n')
    
    while(t>tFinal):
        file.write("Temperatura del sistema: " + str(t)+'\n')
        file.write("Iteracion: " + str(cont)+'\n')
        cont = cont + 1
        it = (t/l)*n #L
        file.write("--- Total subiteraciones NR: " + str(it)+'\n')
        it = int(round(it))+1                                                   #para los casos en los que obtengo 0
        file.write("--- Total subiteraciones R: " + str(it)+'\n')
        
        for i in range (0,it):
            f = dcel.faces[random.randint(0,n-1)]                               #select random face
            color = f.color
            oldPolygons = fV.vorFinitePolygonsList(vor)                         #not delimited
            newPoint = tM.disturbPoint(f.point, f.polygon)           #calculate new point
            file.write("------ Subiteracion num: " + str(i)+'\n')
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point                                                 #save old point
            f.point = newPoint                                                  #change old -> new
            pSet = dcel.points()                                                #rescue all points with new point
            vor = Voronoi(pSet)                                                 #recalculate voronoi
            newPolygons = fV.vorFinitePolygonsList(vor)                         #not delimited
            
            comp = sDif.orChainColours(dcel.faces, oldPolygons, newPolygons, color, box)
            
            if comp: #or chain
                file.write("Energia local mejorada con nuevo punto : " + str(newPoint)+'\n')
            else:
                file.write("Energia local no mejorada, tampoco aceptada "+'\n')
                f.point = savePoint
                pSet = dcel.points()
                vor = Voronoi(pSet)
                
            sD = sDif.symDif(dcel, polygons, box)
            if (sD < bestSD):                                                   #if best solution
                bestSD = sD                                                     #best symmetric difference <- actual symmetric difference
                bestSet = pSet                                                  #best set of generator points <- actual set of generator points
            
            if (not static):
                pS.distroPoints(dcel, mode, box.bounds[2], box.bounds[3])
            
        t = t*r
    file.close
    
    #last it
    polygons = fV.vorFinitePolygonsList(vor)
    pSet = dcel.points()
    sD =  sDif.symDif(dcel, polygons, box)
    
    return bestSet, bestSD, pSet, sD 




def simulatedAnnealingColours_NumbersMethod(dcel, pointsSet, vorDiagram, polygonsList, sDini, ratio, tInicial, tFinal, l, n, minRandom, maxRandom, box, mode, static):
         
    file = open("sA_colours_numbers.txt","w") 
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING COLOURS NUMBERS METHOD")
    
    pSet = pointsSet                                                             
    vor = vorDiagram                                                            
    polygons = polygonsList                                                     
    sD = sDini                                                                 
    
    bestSD = sD
    bestSet = pSet                                                              #best set of points solution
     
    cont = 0
    t = tInicial                                                                #|negative|
    r = ratio                                                                   # + m.log10(n)
 
    pS.distroPoints(dcel, mode, box.bounds[2], box.bounds[3])
    
    file.write("Number of generating points: " + str(len(pSet))+'\n')
    file.write("Number of faces: " + str(n)+'\n')
    
    while(t>tFinal):
        file.write("Temperatura del sistema: " + str(t)+'\n')
        file.write("Iteracion: " + str(cont)+'\n')
        cont = cont + 1
        it = (t/l)*n #L
        file.write("--- Total subiteraciones NR: " + str(it)+'\n')
        it = int(round(it))+1                                                   #para los casos en los que obtengo 0
        file.write("--- Total subiteraciones R: " + str(it)+'\n')
        
        for i in range (0,it):
            f = dcel.faces[random.randint(0,n-1)]                               #select random face
            color = f.color
            oldPolygons = fV.vorFinitePolygonsList(vor)                         #not delimited
            oldLocalSD = sDif.miniSymDif(f, polygons, box)/box.area
            oldSD = sDif.symDifColours(dcel.faces, oldPolygons, color, box,  box.bounds[2], box.bounds[3])
            newPoint = tM.disturbPoint(f.point, f.polygon)           #calculate new point
            file.write("------ Subiteracion num: " + str(i)+'\n')
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point                                                 #save old point
            f.point = newPoint                                                  #change old -> new
            pSet = dcel.points()                                                #rescue all points with new point
            vor = Voronoi(pSet)                                                 #recalculate voronoi
            newPolygons = fV.vorFinitePolygonsList(vor)                         #not delimited
            newLocalSD = sDif.miniSymDif(f, polygons, box)/box.area
            newSD = sDif.symDifColours(dcel.faces, newPolygons, color, box,  box.bounds[2], box.bounds[3])
            
            better, worse = sDif.numbersColours(dcel.faces, oldPolygons, newPolygons, color, box)
            file.write(str(better)+'\n')
            file.write(str(worse)+'\n')
            
            if better >= worse: 
                file.write("Energia local mejorada con nuevo punto : " + str(newPoint)+'\n')
            elif better == worse:
                if (newLocalSD <= oldLocalSD):
                    file.write("Energia local mejorada en el caso 1 con nuevo punto : " + str(newPoint)+'\n')
                else:
                    delta = newSD - oldSD
                    prob = m.e**(-delta/t)
                    rand = np.random.uniform(minRandom, maxRandom)
                    if(rand > prob):
                        file.write("Energia local no mejorada en el caso 1 pero aceptada "+'\n')
                    else:
                        file.write("Energia local no mejorada en el caso 1, tampoco aceptada "+'\n')
                        f.point = savePoint
                        pSet = dcel.points()
                        vor = Voronoi(pSet)
            else: #elif better > worse:
                delta = newSD - oldSD
                prob = m.e**(-delta/t)
                rand = np.random.uniform(minRandom, maxRandom)
                if(rand > prob):
                    file.write("Energia local no mejorada pero aceptada "+'\n')
                else:
                    file.write("Energia local no mejorada, tampoco aceptada "+'\n')
                    f.point = savePoint
                    pSet = dcel.points()
                    vor = Voronoi(pSet)
                
            polygons = fV.vorFinitePolygonsList(vor)    
            sD = sDif.symDif(dcel, polygons, box)
            if (sD < bestSD):                                               #if best solution
                bestSD = sD                                                 #best symmetric difference <- actual symmetric difference
                bestSet = pSet                                              #best set of generator points <- actual set of generator points
            
            if (not static):
                pS.distroPoints(dcel, mode, box.bounds[2], box.bounds[3])
            
        t = t*r
    file.close
    
    #last it
    pSet = dcel.points()
    sD =  sDif.symDif(dcel, polygons, box)
    
    return bestSet, bestSD, pSet, sD 

