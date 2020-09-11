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


def simulatedAnnealingGroups_AndMethod(dcel, ratio, tInicial, tFinal, l, n, minRandom, maxRandom):
         
    file = open("tmp/sA_groups_and.txt","w")
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING GROUPS AND METHOD")
    
    box = dcel.box
    pSet = dcel.points()                                                            
    vor = Voronoi(pSet)                                                            
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)                                                     
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)                                                                 
    
    bestsDs = []
    sDs = []
    temps = []
    its = []

    bestSD = sD
    bestSet = None #best set of points solution
     
    cont = 0
    t = tInicial #|negative|
    r = ratio # + math.log10(n)
    
    oldSDs = [] #aux
    newSDs = []
    res = [] #cadena de ands
    numMejoras = 0 #contador de mejoras (number of improvements)

   
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
            file.write("------ Subiteracion num: " + str(i)+'\n')
            f = dcel.faces[random.randint(0,n-1)] #select random face
            numW = f.numEdges()
            oldSDs.append(symmetricDifference.localSymDif(f, polygons, box)/box.area) #add symDif of selected point/face
            polygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            file.write("------------ oldPoint: " + str(f.point)+'\n')
            file.write("-------------------- oldSD: " + str(oldSDs[0]) +'\n')
            
            index = 1 #empezamos a contar en uno ya que está incluida la DS del nodo central
            w = f.wedge
            for i in range (0, numW):
                tF = w.twin.face
                if(not tF.external):
                    oldSDs.append(symmetricDifference.localSymDif(tF, polygons, box)/box.area)  #add symDif of selected point/face
                    file.write("------------ neighbour point " + str(i) + " : " + str(tF.point)+'\n')
                    file.write("-------------------- oldSD: " + str(oldSDs[index]) +'\n')
                    index = index + 1
                w = w.nexthedge
            
            newPoint = toolsModule.disturbPoint(f.point, f.polygon) #calculate new point
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point #save old point
            f.point = newPoint #change old -> new
            pSet = dcel.points() #rescue all points with new point
            vor = Voronoi(pSet) #recalculate voronoi
            polygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            newSDs.append(symmetricDifference.localSymDif(f, polygons, box)/box.area) #add symDif of selected point/face
            
            index = 1
            w = f.wedge
            for j in range (0, numW):
                tF = w.twin.face
                if(not tF.external):
                    newSDs.append(symmetricDifference.localSymDif(tF, polygons, box)/box.area) #add symDif of selected point/face
                    file.write("------------ neighbour point " + str(j) + " : " + str(tF.point)+'\n')
                    file.write("-------------------- simSD: " + str(oldSDs[index]) +'\n')
                    index = index + 1
                w = w.nexthedge
    
            size = len(oldSDs) #no necesariamente será num Aristas + 1 ya que no se trabaja con las caras externas
    
            file.write("------------------------- COMPARATOR\n'")
            for k in range (0, size): #observamos resultados
                old = oldSDs[k]
                new = newSDs[k]
                b = new<=old
                res.append(b)
                if (b):
                    numMejoras += 1
                file.write("------------------------------ posVector: " + str(k))
                file.write(" new : " + str(new) +'>=')
                file.write(" old : " + str(old) +'?:')
                file.write(" " + str(b) +'\n')
            
            file.write("------------------------- RESULTADO'\n'")
            file.write("------------------------------------- numero de implicados: "+ str(size)+'\n')
            file.write("------------------------------------- numero de mejoras: " + str(numMejoras)+'\n')

            if size == numMejoras: #and                                           
                file.write("----------------------------------------- ACEPTADO "+'\n')
            else:
                file.write("----------------------------------------- DENEGADO "+'\n')
                file.write("-------------------------------------------- Segunda oportunidad: "+'\n')
                delta = toolsModule.sumatorio(newSDs)-toolsModule.sumatorio(oldSDs) #decide número mejoras
                prob = math.e**(-delta/t)
                rand = numpy.random.uniform(minRandom,maxRandom)
                if(rand > prob):
                    file.write("-------------------------------------------- ACEPTADO "+'\n')
                else:
                    file.write("-------------------------------------------- DENEGADO "+'\n')
                    f.point = savePoint
                    pSet = dcel.points()
                    vor = Voronoi(pSet)
            
            sD = symmetricDifference.symDif(dcel.faces, polygons, box)
            if (sD < bestSD): #if best solution
                bestSD = sD #best symmetric difference <- actual symmetric difference
                bestSet = pSet #best set of generator points <- actual set of generator points
                    
            bestsDs.append(bestSD)
            sDs.append(sD)
            temps.append(t)
            its.append(i)

            oldSDs = [] #reboot
            newSDs = []
            res = []                                                                    
            numMejoras = 0

        t = t*r
        
    file.close
    
    #last it
    pSet = dcel.points()
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)
    
    return bestSet, bestSD, bestsDs, sDs, temps, its



def simulatedAnnealingGroups_OrMethod(dcel, ratio, tInicial, tFinal, l, n, minRandom, maxRandom):
         
    file = open("tmp/sA_groups_or.txt","w")
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING GROUPS OR METHOD")
    
    box = dcel.box
    pSet = dcel.points()                                                            
    vor = Voronoi(pSet)                                                            
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)                                                     
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)                                                                 
    
    bestsDs = []
    sDs = []
    temps = []
    its = []

    bestSD = sD
    bestSet = pSet #best set of points solution
     
    cont = 0
    t = tInicial #|negative|
    r = ratio # + math.log10(n)
    
    oldSDs = [] #aux
    newSDs = []
    res = [] #cadena de ands
    numMejoras = 0 #contador de mejoras (number of improvements)

    
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
            #print(i)
            file.write("------ Subiteracion num: " + str(i)+'\n')
            f = dcel.faces[random.randint(0,n-1)] #select random face
            numW = f.numEdges()
            oldSDs.append(symmetricDifference.localSymDif(f, polygons, box)/box.area) #add symDif of selected point/face
            polygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            file.write("------------ oldPoint: " + str(f.point)+'\n')
            file.write("-------------------- oldSD: " + str(oldSDs[0]) +'\n')
            
            index = 1 #empezamos a contar en uno ya que está incluida la DS del nodo central
            w = f.wedge
            for i in range (0, numW):
                tF = w.twin.face
                if(not tF.external):
                    oldSDs.append(symmetricDifference.localSymDif(tF, polygons, box)/box.area) #add symDif of selected point/face
                    file.write("------------ neighbour point " + str(i) + " : " + str(tF.point)+'\n')
                    file.write("-------------------- oldSD: " + str(oldSDs[index]) +'\n')
                    index = index + 1
                w = w.nexthedge
            
            newPoint = toolsModule.disturbPoint(f.point, f.polygon) #calculate new point
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point #save old point
            f.point = newPoint #change old -> new
            pSet = dcel.points() #rescue all points with new point
            vor = Voronoi(pSet) #recalculate voronoi
            polygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            newSDs.append(symmetricDifference.localSymDif(f, polygons, box)/box.area) #add symDif of selected point/face
            
            index = 1
            w = f.wedge
            for j in range (0, numW):
                tF = w.twin.face
                if(not tF.external):
                    newSDs.append(symmetricDifference.localSymDif(tF, polygons, box)/box.area)  #add symDif of selected point/face
                    file.write("------------ neighbour point " + str(j) + " : " + str(tF.point)+'\n')
                    file.write("-------------------- simSD: " + str(oldSDs[index]) +'\n')
                    index = index + 1
                w = w.nexthedge
    
            size = len(oldSDs) #no necesariamente será num Aristas + 1 ya que no se trabaja con las caras externas

    
            file.write("------------------------- COMPARATOR'\n'")
            for k in range (0, size): #observamos resultados
                old = oldSDs[k]
                new = newSDs[k]
                b = new<=old
                res.append(b)
                if (b):
                    numMejoras += 1
                file.write("------------------------------ posVector: " + str(k))
                file.write(" new : " + str(new) +'>=')
                file.write(" old : " + str(old) +'?:')
                file.write(" " + str(b) +'\n')
            
            file.write("------------------------- RESULTADO'\n'")
            file.write("------------------------------------- numero de implicados: "+ str(size)+'\n')
            file.write("------------------------------------- numero de mejoras: " + str(numMejoras)+'\n')

            if numMejoras != 0: #or                                                
                file.write("----------------------------------------- ACEPTADO "+'\n')
            else:
                file.write("----------------------------------------- DENEGADO "+'\n')
                f.point = savePoint
                pSet = dcel.points()
                vor = Voronoi(pSet)

            sD = symmetricDifference.symDif(dcel.faces, polygons, box)
            if (sD < bestSD):  #if best solution
                bestSD = sD  #best symmetric difference <- actual symmetric difference
                bestSet = pSet #best set of generator points <- actual set of generator points
                    
            bestsDs.append(bestSD)
            sDs.append(sD)
            temps.append(t)
            its.append(i)

            oldSDs = [] #reboot
            newSDs = []
            res = []                                                                    
            numMejoras = 0 

        t = t*r
        
    file.close
    
    #last it
    pSet = dcel.points()
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)
    
    return bestSet, bestSD, bestsDs, sDs, temps, its



def simulatedAnnealingGroups_NumbersMethod(dcel, ratio, tInicial, tFinal, l, n, minRandom, maxRandom):
         
    file = open("tmp/sA_groups_numbers.txt","w")
    file.flush
    
    print("Ejecutando SIMULATED ANNEALING GROUPS NUMBERS METHOD")
    
    box = dcel.box
    pSet = dcel.points()                                                            
    vor = Voronoi(pSet)                                                            
    polygons = finiteVoronoi.vorFinitePolygonsList(vor)                                                     
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)                                                                 
    
    bestsDs = []
    sDs = []
    temps = []
    its = []

    bestSD = sD
    bestSet = None #best set of points solution
     
    cont = 0
    t = tInicial #|negative|
    r = ratio # + math.log10(n)
    
    oldSDs = [] #aux
    newSDs = []
    res = [] #cadena de ands
    numMejoras = 0 #contador de mejoras (number of improvements)

    
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
            file.write("------ Subiteracion num: " + str(i)+'\n')
            f = dcel.faces[random.randint(0,n-1)] #select random face
            numW = f.numEdges()
            oldSDs.append(symmetricDifference.localSymDif(f, polygons, box)/box.area) #add symDif of selected point/face
            polygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            file.write("------------ oldPoint: " + str(f.point)+'\n')
            file.write("-------------------- oldSD: " + str(oldSDs[0]) +'\n')
            
            index = 1 #empezamos a contar en uno ya que está incluida la DS del nodo central
            w = f.wedge
            for i in range (0, numW):
                tF = w.twin.face
                if(not tF.external):
                    oldSDs.append(symmetricDifference.localSymDif(tF, polygons, box)/box.area) #add symDif of selected point/face
                    file.write("------------ neighbour point " + str(i) + " : " + str(tF.point)+'\n')
                    file.write("-------------------- oldSD: " + str(oldSDs[index]) +'\n')
                    index = index + 1
                w = w.nexthedge
            
            newPoint = toolsModule.disturbPoint(f.point, f.polygon) #calculate new point
            file.write("------------ newPoint: " + str(newPoint)+'\n')
            savePoint = f.point #save old point
            f.point = newPoint #change old -> new
            pSet = dcel.points() #rescue all points with new point
            vor = Voronoi(pSet) #recalculate voronoi
            polygons = finiteVoronoi.vorFinitePolygonsList(vor) #not delimited
            newSDs.append(symmetricDifference.localSymDif(f, polygons, box)/box.area) #add symDif of selected point/face
            
            index = 1
            w = f.wedge
            for j in range (0, numW):
                tF = w.twin.face
                if(not tF.external):
                    newSDs.append(symmetricDifference.localSymDif(tF, polygons, box)/box.area) #add symDif of selected point/face
                    file.write("------------ neighbour point " + str(j) + " : " + str(tF.point)+'\n')
                    file.write("-------------------- simSD: " + str(oldSDs[index]) +'\n')
                    index = index + 1
                w = w.nexthedge
    
            size = len(oldSDs) #no necesariamente será num Aristas + 1 ya que no se trabaja con las caras externas
    
            file.write("------------------------- COMPARATOR'\n'")
            for k in range (0, size): #observamos resultados
                old = oldSDs[k]
                new = newSDs[k]
                b = new<=old
                res.append(b)
                if (b):
                    numMejoras += 1
                file.write("------------------------------ posVector: " + str(k))
                file.write(" new : " + str(new) +'>=')
                file.write(" old : " + str(old) +'?:')
                file.write(" " + str(b) +'\n')
            
            file.write("------------------------- RESULTADO'\n'")
            file.write("------------------------------------- numero de implicados: "+ str(size)+'\n')
            file.write("------------------------------------- numero de mejoras: " + str(numMejoras)+'\n')


            if numMejoras > size/2:                                                
                file.write("----------------------------------------- ACEPTADO "+'\n')
            elif numMejoras == size/2:
                if newSDs[0] >= oldSDs[0]: #if selected face improves
                    file.write("----------------------------------------- ACEPTADO "+'\n')
                else:
                    file.write("----------------------------------------- DENEGADO "+'\n')
                    file.write("-------------------------------------------- Segunda oportunidad: "+'\n')
                    delta = toolsModule.sumatorio(newSDs)-toolsModule.sumatorio(oldSDs) #decide número mejoras
                    prob = math.e**(-delta/t)
                    rand = numpy.random.uniform(minRandom,maxRandom)
                    if(rand > prob):
                        file.write("-------------------------------------------- ACEPTADO "+'\n')
                    else:
                        file.write("-------------------------------------------- DENEGADO "+'\n')
                        f.point = savePoint
                        pSet = dcel.points()
                        vor = Voronoi(pSet)
            else:
                file.write("----------------------------------------- DENEGADO "+'\n')
                file.write("-------------------------------------------- Segunda oportunidad: "+'\n')
                delta = toolsModule.sumatorio(newSDs)-toolsModule.sumatorio(oldSDs) #decide número mejoras
                prob = math.e**(-delta/t)
                rand = numpy.random.uniform(minRandom,maxRandom)
                if(rand > prob):
                    file.write("-------------------------------------------- ACEPTADO "+'\n')
                else:
                    file.write("-------------------------------------------- DENEGADO "+'\n')
                    f.point = savePoint
                    pSet = dcel.points()
                    vor = Voronoi(pSet)


            sD = symmetricDifference.symDif(dcel.faces, polygons, box)
            if (sD < bestSD):  #if best solution
                bestSD = sD #best symmetric difference <- actual symmetric difference
                bestSet = pSet #best set of generator points <- actual set of generator points
            
            bestsDs.append(bestSD)
            sDs.append(sD)
            temps.append(t)
            its.append(i)

            oldSDs = [] #reboot
            newSDs = []
            res = []                                                                    
            numMejoras = 0

        t = t*r
        
    file.close
    
    #last it
    pSet = dcel.points()
    sD =  symmetricDifference.symDif(dcel.faces, polygons, box)
    
    return bestSet, bestSD, bestsDs, sDs, temps, its
