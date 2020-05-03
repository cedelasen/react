#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#José María de la Sen Molina, @cedelasen

from scipy.spatial import Voronoi
import math as m
import numpy as np
import toolsModule as tM
import finiteVor as fV
import symDif as sDif
import random


def simulatedAnnealing(dcel, pointsSet, vorDiagram, polygonsList, sDini, ratio, tInicial, tFinal, l, n, minRandom, maxRandom, box):
         
    file = open("sA_classic.txt","w") 
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING CLASSIC")
    
    pSet = []                                                                   #points set
    pSet = dcel.points()                                                        #rescue all points (previous planting seeds)
    vor = Voronoi(pSet)                                                         #calculate voronoi
    polygons = fV.vorFinitePolygonsList(vor)                                    #vor to finiteVor (polygons) // list of polygons -> sin delimitar
    sD =  sDif.symDif(dcel, polygons, box)                                      #initial energy (global)
    
    bestSet = pSet                                                              #best set of points solution                                               
    bestSD = sD                                                                 #best symmetric difference solution
     
    cont = 0
    t = m.fabs(1/m.log10(sD))                                                   #|negative|
    n = len(dcel.faces)                                                         #29 (Palop)
    r = ratio                                                                   # + m.log10(n)
    tFinal = t/(100*m.log10(n))                                                 #frozen
    
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
            polygons = fV.vorFinitePolygonsList(vor)                            #not delimited
            localSD = sDif.miniSymDif(f, polygons, box)/box.area                #local symmetric difference
            file.write("------ Subiteracion num: " + str(i)+'\n')
            newPoint = tM.disturbPoint(f.point, f.polygon)           #calculate new point
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point                                                 #save old point
            f.point = newPoint                                                  #change old -> new
            pSet = dcel.points()                                                #rescue all points with new point
            vor = Voronoi(pSet);                                                #recalculate voronoi
            polygons = fV.vorFinitePolygonsList(vor)                            #not delimited
            newLocalSD = sDif.miniSymDif(f, polygons, box)/box.area             #new local symmetric difference
            if (newLocalSD < localSD):                                          #if better solution
                file.write("Energia local mejorada con nuevo punto : " + str(newPoint)+'\n')
            else:                                                               #else ... worse solution, function acceptance
                file.write("Energia local no mejorada con nuevo punto : " + str(newPoint)+'\n')
                delta = newLocalSD - localSD
                prob = m.e**(-delta/t)
                rand = np.random.uniform(minRandom,maxRandom)
                if(rand > prob):
                    file.write("Energia local no mejorada pero aceptada "+'\n')
                else:
                    file.write("Energia local no mejorada, tampoco aceptada "+'\n')
                    f.point = savePoint
                    pSet = dcel.points()
                    vor = Voronoi(pSet)
                    
            sD = sDif.symDif(dcel, polygons, box)
            if (sD < bestSD):                                                   #if best solution
                bestSD = sD                                                     #best symmetric difference <- actual symmetric difference
                bestSet = pSet                                                  #best set of generator points <- actual set of generator points
            
        t = t*r
    file.close
    
    #last it
    pSet = dcel.points()
    sD =  sDif.symDif(dcel, polygons, box)
    
    return bestSet, bestSD, pSet, sD

# def simulatedAnnealingOld(dcel, ratio, iniX, finX, iniY, finY, box):
         
#     file = open("sA.txt","w") 
#     file.flush
    
#     print("Ejecutando SIMULATED ANNEALING")
    
#     pSet = []                                                                   #points set
#     pSet = dcel.points()                                                        #rescue all points (previous planting seeds)
#     vor = Voronoi(pSet)                                                         #calculate voronoi
#     polygons = fV.vorFinitePolygonsList(vor)                                    #vor to finiteVor (polygons) // list of polygons -> sin delimitar
#     sD =  sDif.symDif(dcel, polygons, box)                                      #initial energy
    
#     bestSet = pSet                                                              #best set of points solution                                               
#     bestSD = sD                                                                 #best symmetric difference solution
     
#     cont = 0
#     t = m.fabs(1/m.log10(sD))                                                   #|negative|
#     n = len(dcel.faces)                                                         
#     r = ratio                                                                   # + m.log10(n)
#     tFinal = t/(100*m.log10(n))                                                 #frozen
    
#     #print("Number of generating points: ", len(pSet))
#     file.write("Number of generating points: " + str(len(pSet))+'\n')
#     #print("Number of faces: ", n)
#     file.write("Number of faces: " + str(n)+'\n')
    
#     while(t>tFinal):
#         #print("Temperatura del sistema: ", t)
#         file.write("Temperatura del sistema: " + str(t)+'\n')
#         #print("Iteracion: ", cont)
#         file.write("Iteracion: " + str(cont)+'\n')
#         cont = cont + 1
#         it = (t/0.06)*n #L
#         #print("--- Total subiteraciones NR: ", it)
#         file.write("--- Total subiteraciones NR: " + str(it)+'\n')
#         it = int(round(it))+1                                                   #para los casos en los que obtengo 0
#         #print("--- Total subiteraciones R: ", it)
#         file.write("--- Total subiteraciones R: " + str(it)+'\n')
#         for i in range (0,it):
#             f = dcel.faces[random.randint(0,n-1)]                               #select random face
#             #print("------ Subiteracion num: ", i)
#             file.write("------ Subiteracion num: " + str(i)+'\n')
#             newPoint = tM.disturbPoint(f.point, f.polygon)           #calculate new point
#             #print("------------ newPoint: ", newPoint)
#             file.write("------------ newPoint: " + str(newPoint)+'\n')
#             savePoint = f.point                                                 #save old point
#             f.point = newPoint                                                  #change old -> new
#             pSet = dcel.points()                                                #rescue all points with new point
#             vor = Voronoi(pSet);                                                #recalculate voronoi
#             polygons = fV.vorFinitePolygonsList(vor)
#             newSD =  sDif.symDif(dcel, polygons, box)                           #new energy
#             if (newSD < sD):                                                    #if better solution
#                 #print("Energia mejorada con nuevo punto : ", newPoint)
#                 file.write("Energia mejorada con nuevo punto : " + str(newPoint)+'\n')
#                 #print("Nueva energia: ", newSD)
#                 file.write("Nueva energia: "+ str(newSD)+'\n')
#                 sD = newSD 
#                 if (sD < bestSD):                                               #if best solution
#                     bestSD = sD                                                 #best symmetric difference <- actual symmetric difference
#                     bestSet = pSet                                              #best set of generator points <- actual set of generator points
#             else:                                                               #else ... worse solution, function acceptance
#                 #print("Energia no mejorada con nuevo punto : ", newPoint)
#                 file.write("Energia no mejorada con nuevo punto : " + str(newPoint)+'\n')
#                 delta = newSD - sD
#                 prob = m.e**(-delta/t)
#                 rand = np.random.uniform(0,1)
#                 if(rand > prob):
#                     #print("Energia no mejorada pero aceptada ")
#                     file.write("Energia no mejorada pero aceptada "+'\n')
#                     #print("Nueva energia: ", newSD)
#                     file.write("Nueva energia: "+ str(newSD)+'\n')
#                     sD = newSD
#                 else:
#                     #print("Energia no mejorada, tampoco aceptada ")
#                     file.write("Energia no mejorada, tampoco aceptada "+'\n')
#                     #print("Vieja y mantenida energia: ", sD)
#                     file.write("Vieja y mantenida energia: "+ str(newSD)+'\n')
#                     f.point = savePoint    
#         t = t*r
#     file.close
#     return bestSet, bestSD, pSet, sD                                            #returns the best and the actual set of genPoints/symmetric difference

