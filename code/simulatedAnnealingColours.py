"""
@author: cedelasen
"""

import finiteVoronoi
import math
import numpy
import plantingSeeds
import random
import symmetricDifference
import toolsModule
from scipy.spatial import (
    Voronoi
)


def simulatedAnnealingColours_AndMethod(dcel, ratio, tInicial, tFinal, l, n, minRandom, maxRandom, mode, static):
         
    file = open("tmp/sA_colours_and.txt","w") 
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING COLOURS AND METHOD")
    
    box = dcel.box
    pSet = dcel.points()                                                            
    vor = Voronoi(pSet)                                                            
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)                                                     
    sD = symmetricDifference.symDif(dcel.faces, polygons, box)                                                               
    
    sDs = []
    temps = []
    its = []

    bestSD = sD
    bestSet = pSet #best set of points solution
     
    cont = 0
    t = tInicial #|negative|
    r = ratio # + m.log10(n)
    
    plantingSeeds.distroPoints(dcel, mode)
    
    file.write("Number of generating points: " + str(len(pSet))+'\n')
    file.write("Number of faces: " + str(n)+'\n')
    
    while(t>tFinal):
        file.write("Temperatura del sistema: " + str(t)+'\n')
        file.write("Iteracion: " + str(cont)+'\n')
        cont = cont + 1
        it = (t/l)*n #L
        file.write("--- Total subiteraciones NR: " + str(it)+'\n')
        it = int(round(it))+1 #para los casos en los que obtengo 0
        file.write("--- Total subiteraciones R: " + str(it)+'\n')
        
        for i in range (0,it):
            f = dcel.faces[random.randint(0,n-1)] #select random face
            color = f.color
            oldPolygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            oldSD = symmetricDifference.symDifColours(dcel.faces, oldPolygons, color, box)
            newPoint = toolsModule.disturbPoint(f.point, f.polygon) #calculate new point
            file.write("------ Subiteracion num: " + str(i)+'\n')
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point #save old point
            f.point = newPoint #change old -> new
            pSet = dcel.points() #rescue all points with new point
            vor = Voronoi(pSet) #recalculate voronoi
            newPolygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            newSD = symmetricDifference.symDifColours(dcel.faces, newPolygons, color, box)
            
            comp = symmetricDifference.andChainColours(dcel.faces, oldPolygons, newPolygons, color, box)
            
            if comp: #and chain
                file.write("Energia local mejorada con nuevo punto : " + str(newPoint)+'\n')
            else:
                delta = newSD - oldSD
                prob = math.e**(-delta/t)
                rand = numpy.random.uniform(minRandom, maxRandom)
                if(rand > prob):
                    file.write("Energia local no mejorada pero aceptada "+'\n')
                else:
                    file.write("Energia local no mejorada, tampoco aceptada "+'\n')
                    f.point = savePoint
                    pSet = dcel.points()
                    vor = Voronoi(pSet)
                    
            sD = symmetricDifference.symDif(dcel.faces, polygons, box)
            if (sD < bestSD): #if best solution
                bestSD = sD #best symmetric difference <- actual symmetric difference
                bestSet = pSet #best set of generator points <- actual set of generator points
            
            sDs.append(bestSD)
            temps.append(t)
            its.append(it)

            if (not static):
                plantingSeeds.distroPoints(dcel, mode)
            
        t = t*r
    file.close
    
    #last it
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)
    pSet = dcel.points()
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)
    
    return bestSet, bestSD, sDs, temps, its




def simulatedAnnealingColours_OrMethod(dcel, ratio, tInicial, tFinal, l, n, minRandom, maxRandom, mode, static):
         
    file = open("tmp/sA_colours_or.txt","w") 
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING COLOURS OR METHOD")
    
    box = dcel.box
    pSet = dcel.points()                                                            
    vor = Voronoi(pSet)                                                            
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)                                                     
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)                                                                 
    
    sDs = []
    temps = []
    its = []

    bestSD = sD
    bestSet = pSet #best set of points solution
     
    cont = 0
    t = tInicial #|negative|
    r = ratio # + m.log10(n)
    
    plantingSeeds.distroPoints(dcel, mode)
    
    file.write("Number of generating points: " + str(len(pSet))+'\n')
    file.write("Number of faces: " + str(n)+'\n')
    
    while(t>tFinal):
        file.write("Temperatura del sistema: " + str(t)+'\n')
        file.write("Iteracion: " + str(cont)+'\n')
        cont = cont + 1
        it = (t/l)*n #L
        file.write("--- Total subiteraciones NR: " + str(it)+'\n')
        it = int(round(it))+1 #para los casos en los que obtengo 0
        file.write("--- Total subiteraciones R: " + str(it)+'\n')
        
        for i in range (0,it):
            f = dcel.faces[random.randint(0,n-1)] #select random face
            color = f.color
            oldPolygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            newPoint = toolsModule.disturbPoint(f.point, f.polygon) #calculate new point
            file.write("------ Subiteracion num: " + str(i)+'\n')
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point #save old point
            f.point = newPoint #change old -> new
            pSet = dcel.points() #rescue all points with new point
            vor = Voronoi(pSet) #recalculate voronoi
            newPolygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            
            comp = symmetricDifference.orChainColours(dcel.faces, oldPolygons, newPolygons, color, box)
            
            if comp: #or chain
                file.write("Energia local mejorada con nuevo punto : " + str(newPoint)+'\n')
            else:
                file.write("Energia local no mejorada, tampoco aceptada "+'\n')
                f.point = savePoint
                pSet = dcel.points()
                vor = Voronoi(pSet)
                
            sD = symmetricDifference.symDif(dcel.faces, polygons, box)
            if (sD < bestSD): #if best solution
                bestSD = sD #best symmetric difference <- actual symmetric difference
                bestSet = pSet #best set of generator points <- actual set of generator points
            
            sDs.append(bestSD)
            temps.append(t)
            its.append(it)

            if (not static):
                plantingSeeds.distroPoints(dcel, mode)
            
        t = t*r
    file.close
    
    #last it
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)
    pSet = dcel.points()
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)
    
    return bestSet, bestSD, sDs, temps, its




def simulatedAnnealingColours_NumbersMethod(dcel, ratio, tInicial, tFinal, l, n, minRandom, maxRandom, mode, static):
         
    file = open("tmp/sA_colours_numbers.txt","w") 
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING COLOURS NUMBERS METHOD")

    box = dcel.box
    pSet = dcel.points()                                                            
    vor = Voronoi(pSet)                                                            
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)                                                     
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)                                                                 
    
    sDs = []
    temps = []
    its = []

    bestSD = sD
    bestSet = pSet #best set of points solution
     
    cont = 0
    t = tInicial #|negative|
    r = ratio # + m.log10(n)
 
    plantingSeeds.distroPoints(dcel, mode)
    
    file.write("Number of generating points: " + str(len(pSet))+'\n')
    file.write("Number of faces: " + str(n)+'\n')
    
    while(t>tFinal):
        file.write("Temperatura del sistema: " + str(t)+'\n')
        file.write("Iteracion: " + str(cont)+'\n')
        cont = cont + 1
        it = (t/l)*n #L
        file.write("--- Total subiteraciones NR: " + str(it)+'\n')
        it = int(round(it))+1 #para los casos en los que obtengo 0
        file.write("--- Total subiteraciones R: " + str(it)+'\n')
        
        for i in range (0,it):
            f = dcel.faces[random.randint(0,n-1)] #select random face
            color = f.color
            oldPolygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            oldLocalSD = symmetricDifference.localSymDif(f, polygons, box)/box.area
            oldSD = symmetricDifference.symDifColours(dcel.faces, oldPolygons, color, box)
            newPoint = toolsModule.disturbPoint(f.point, f.polygon) #calculate new point
            file.write("------ Subiteracion num: " + str(i)+'\n')
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point #save old point
            f.point = newPoint #change old -> new
            pSet = dcel.points() #rescue all points with new point
            vor = Voronoi(pSet) #recalculate voronoi
            newPolygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            newLocalSD = symmetricDifference.localSymDif(f, polygons, box)/box.area
            newSD = symmetricDifference.symDifColours(dcel.faces, newPolygons, color, box)
            
            better, worse = symmetricDifference.numbersColours(dcel.faces, oldPolygons, newPolygons, color, box)
            file.write(str(better)+'\n')
            file.write(str(worse)+'\n')
            
            if better >= worse: 
                file.write("Energia local mejorada con nuevo punto : " + str(newPoint)+'\n')
            elif better == worse:
                if (newLocalSD <= oldLocalSD):
                    file.write("Energia local mejorada en el caso 1 con nuevo punto : " + str(newPoint)+'\n')
                else:
                    delta = newSD - oldSD
                    prob = math.e**(-delta/t)
                    rand = numpy.random.uniform(minRandom, maxRandom)
                    if(rand > prob):
                        file.write("Energia local no mejorada en el caso 1 pero aceptada "+'\n')
                    else:
                        file.write("Energia local no mejorada en el caso 1, tampoco aceptada "+'\n')
                        f.point = savePoint
                        pSet = dcel.points()
                        vor = Voronoi(pSet)
            else: #elif better > worse:
                delta = newSD - oldSD
                prob = math.e**(-delta/t)
                rand = numpy.random.uniform(minRandom, maxRandom)
                if(rand > prob):
                    file.write("Energia local no mejorada pero aceptada "+'\n')
                else:
                    file.write("Energia local no mejorada, tampoco aceptada "+'\n')
                    f.point = savePoint
                    pSet = dcel.points()
                    vor = Voronoi(pSet)
                
            polygons = finiteVoronoi.vorFinitePolygonsList(vor)    
            sD = symmetricDifference.symDif(dcel.faces, polygons, box)
            if (sD < bestSD): #if best solution
                bestSD = sD #best symmetric difference <- actual symmetric difference
                bestSet = pSet #best set of generator points <- actual set of generator points
            
            sDs.append(bestSD)
            temps.append(t)
            its.append(it)

            if (not static):
                plantingSeeds.distroPoints(dcel, mode)
            
        t = t*r
    file.close
    
    #last it
    pSet = dcel.points()
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)
    
    return bestSet, bestSD, sDs, temps, its

 