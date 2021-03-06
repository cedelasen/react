"""
@author: cedelasen
"""

import finiteVoronoi
import math
import numpy
import random
import symmetricDifference
import toolsModule
from scipy.spatial import (
    Voronoi
)


def simulatedAnnealingPeers_AndMethod(dcel, ratio, tInicial, tFinal, l, n, minRandom, maxRandom):
         
    file = open("tmp/sA_peers_and.txt","w") 
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING PEERS AND METHOD")
    
    box = dcel.box
    pSet = dcel.points()                                                            
    vor = Voronoi(pSet)                                                            
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)                                                     
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)                                                                 
    
    bestsDs = []
    sDs = []
    temps = []
    its = []
    acceptance = []

    bestSD = sD
    bestSet = pSet #best set of points solution
     
    cont = 0
    t = tInicial #|negative|
    r = ratio # + math.log10(n)
    
    file.write("Number of generating points: " + str(len(pSet))+'\n')
    file.write("Number of faces: " + str(n)+'\n')
    
    while(t>tFinal):
        file.write("Temperatura del sistema: " + str(t)+'\n')
        file.write("Iteracion: " + str(cont)+'\n')
        cont = cont + 1
        it = (t/l)*n #L
        file.write("--- Total subiteraciones NR: " + str(it)+'\n')
        it = int(round(it))+1 #0 cases
        file.write("--- Total subiteraciones R: " + str(it)+'\n')
        
        for i in range (0,it):
            f = dcel.faces[random.randint(0,n-1)] #select random face
            peerW = f.randomEdgeNotExt() #random edge not external
            peerF = peerW.twin.face #wedge twin's face
            peerPoint = peerF.point #point to index in the voronoi polygons list
            polygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            localSD_peer1 = symmetricDifference.localSymDif(f, polygons, box)/box.area
            localSD_peer2 = symmetricDifference.localSymDif(peerF, polygons, box)/box.area
            newPoint = toolsModule.disturbPoint(f.point, f.polygon) #calculate new point
            file.write("------ Subiteracion num: " + str(i)+'\n')
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            file.write("------------ peerPoint: " + str(peerPoint)+'\n')
            savePoint = f.point #save old point
            f.point = newPoint #change old -> new
            pSet = dcel.points() #rescue all points with new point
            vor = Voronoi(pSet) #recalculate voronoi
            polygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            newLocalSD_peer1 = symmetricDifference.localSymDif(f, polygons, box)/box.area
            newLocalSD_peer2 = symmetricDifference.localSymDif(peerF, polygons, box)/box.area
            
            if( (newLocalSD_peer1<=localSD_peer1) and (newLocalSD_peer2<=localSD_peer2)): #and chain
                file.write("Energia local mejorada con nuevo punto : " + str(newPoint)+'\n')
                acceptance.append(1)
            else:
                delta = (newLocalSD_peer1+newLocalSD_peer2)-(localSD_peer1+localSD_peer2)
                prob = math.e**(-delta/t)
                rand = numpy.random.uniform(minRandom,maxRandom)
                if(rand > prob):
                    file.write("Energia local no mejorada pero aceptada "+'\n')
                    acceptance.append(1)
                else:
                    file.write("Energia local no mejorada, tampoco aceptada "+'\n')
                    f.point = savePoint
                    pSet = dcel.points()
                    vor = Voronoi(pSet)
                    acceptance.append(0)
                    
            sD = symmetricDifference.symDif(dcel.faces, polygons, box)
            if (sD < bestSD): #if best solution
                bestSD = sD #best symmetric difference <- actual symmetric difference
                bestSet = pSet #best set of generator points <- actual set of generator points
            
            bestsDs.append(bestSD)
            sDs.append(sD)
            temps.append(t)
            its.append(i)

        t = t*r
    file.close
    
    #last it
    pSet = dcel.points()
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)
    
    return bestSet, bestSD, bestsDs, sDs, temps, its, acceptance




def simulatedAnnealingPeers_OrMethod(dcel, ratio, tInicial, tFinal, l, n, minRandom, maxRandom):
         
    file = open("tmp/sA_peers_or.txt","w") 
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING PEERS OR METHOD")
    
    box = dcel.box
    pSet = dcel.points()                                                            
    vor = Voronoi(pSet)                                                            
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)                                                     
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)                                                                 
    
    bestsDs = []
    sDs = []
    temps = []
    its = []
    acceptance = []

    bestSD = sD
    bestSet = pSet #best set of points solution
     
    cont = 0
    t = tInicial #|negative|
    r = ratio # + math.log10(n)
 
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
            peerW = f.randomEdgeNotExt() #random edge not external
            peerF = peerW.twin.face #wedge twin's face
            peerPoint = peerF.point #point to index in the voronoi polygons list
            polygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            localSD_peer1 = symmetricDifference.localSymDif(f, polygons, box)/box.area
            localSD_peer2 = symmetricDifference.localSymDif(peerF, polygons, box)/box.area
            newPoint = toolsModule.disturbPoint(f.point, f.polygon) #calculate new point
            file.write("------ Subiteracion num: " + str(i)+'\n')
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            file.write("------------ peerPoint: " + str(peerPoint)+'\n')
            savePoint = f.point #save old point
            f.point = newPoint #change old -> new
            pSet = dcel.points() #rescue all points with new point
            vor = Voronoi(pSet) #recalculate voronoi
            polygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            newLocalSD_peer1 = symmetricDifference.localSymDif(f, polygons, box)/box.area
            newLocalSD_peer2 = symmetricDifference.localSymDif(peerF, polygons, box)/box.area
            
            if( (newLocalSD_peer1<=localSD_peer1) or (newLocalSD_peer2<=localSD_peer2)): #and chain
                file.write("Energia local mejorada con nuevo punto : " + str(newPoint)+'\n')
                acceptance.append(1)
            else:
                file.write("Energia local no mejorada, tampoco aceptada "+'\n')
                f.point = savePoint
                pSet = dcel.points()
                vor = Voronoi(pSet)
                acceptance.append(0)
                    
            sD = symmetricDifference.symDif(dcel.faces, polygons, box)
            if (sD < bestSD): #if best solution
                bestSD = sD #best symmetric difference <- actual symmetric difference
                bestSet = pSet #best set of generator points <- actual set of generator points
            
            bestsDs.append(bestSD)
            sDs.append(sD)
            temps.append(t)
            its.append(i)

        t = t*r
    file.close
    
    #last it
    pSet = dcel.points()
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)
    
    return bestSet, bestSD, bestsDs, sDs, temps, its, acceptance
