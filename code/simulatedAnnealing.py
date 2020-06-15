"""
@author: cedelasen
"""

import math
import numpy
import toolsModule
import finiteVoronoi
import symmetricDifference
import random
from scipy.spatial import (
    Voronoi
)

def simulatedAnnealing(dcel, ratio, tInicial, tFinal, l, n, minRandom, maxRandom):
         
    file = open("tmp/sA_classic.txt","w") 
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING CLASSIC")
    
    box = dcel.box
    pSet = dcel.points()                                                        #rescue all points (previous planting seeds)
    vor = Voronoi(pSet)                                                         #calculate voronoi
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)                         #vor to finiteVoronoi (polygons) // list of polygons -> sin delimitar
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)                 #initial energy (global)
    
    bestSet = pSet                                                              #best set of points solution                                               
    bestSD = sD                                                                 #best symmetric difference solution
     
    cont = 0
    t = math.fabs(1/math.log10(sD))                                             #|negative|
    n = len(dcel.faces)                                                         #29 (Palop)
    r = ratio                                                                   # + math.log10(n)
    tFinal = t/(100*math.log10(n))                                              #frozen
    
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
            polygons = finiteVoronoi.vorFinitePolygonsList(vor)                 #not delimited
            localSD = symmetricDifference.localSymDif(f, polygons, box)/box.area #local symmetric difference
            file.write("------ Subiteracion num: " + str(i)+'\n')
            newPoint = toolsModule.disturbPoint(f.point, f.polygon)             #calculate new point
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point                                                 #save old point
            f.point = newPoint                                                  #change old -> new
            pSet = dcel.points()                                                #rescue all points with new point
            vor = Voronoi(pSet)                                                 #recalculate voronoi
            polygons = finiteVoronoi.vorFinitePolygonsList(vor)                 #not delimited
            newLocalSD = symmetricDifference.localSymDif(f, polygons, box)/box.area #new local symmetric difference
            if (newLocalSD < localSD):                                          #if better solution
                file.write("Energia local mejorada con nuevo punto : " + str(newPoint)+'\n')
            else:                                                               #else ... worse solution, function acceptance
                file.write("Energia local no mejorada con nuevo punto : " + str(newPoint)+'\n')
                delta = newLocalSD - localSD
                prob = math.e**(-delta/t)
                rand = numpy.random.uniform(minRandom,maxRandom)
                if(rand > prob):
                    file.write("Energia local no mejorada pero aceptada "+'\n')
                else:
                    file.write("Energia local no mejorada, tampoco aceptada "+'\n')
                    f.point = savePoint
                    pSet = dcel.points()
                    vor = Voronoi(pSet)
                    
            sD = symmetricDifference.symDif(dcel.faces, polygons, box)
            if (sD < bestSD):                                                   #if best solution
                bestSD = sD                                                     #best symmetric difference <- actual symmetric difference
                bestSet = pSet                                                  #best set of generator points <- actual set of generator points
            
        t = t*r
    file.close
    
    #last it
    pSet = dcel.points()
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)
    
    return bestSet, bestSD, pSet, sD
