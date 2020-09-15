"""
@author: cedelasen
"""

import dcelInstance
import data
import finiteVoronoi
import math
import plottingModule
import simulatedAnnealing
import simulatedAnnealingPeers
import simulatedAnnealingGroups
import simulatedAnnealingColours
import symmetricDifference

from scipy.spatial import (
    Voronoi,
    voronoi_plot_2d
)

    
def execute(dcel_i, polygons_i, l, r, maxExecs, minR, maxR, relationship, method, coloursDistribution, static, path, it):
 
    dcel = dcel_i
    polygons = polygons_i

    #n
    n = len(dcel.faces) 

    #initial symmetric difference
    sd = symmetricDifference.symDif(dcel.faces, polygons, dcel.box) #initial energy (global)
    
    #T inicial
    tIni = math.fabs(1/math.log10(sd))
    
    #T final
    tFin = tIni/(100*math.log10(n))
        

    #################################   SELECTOR   ##################################
    #Execution switch
    if (relationship == "classic"):
        bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = simulatedAnnealing.simulatedAnnealing(dcel, r, tIni, tFin, l, n, minR, maxR)
    elif (relationship == "peers"):
        if (method == "and"):
            bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = simulatedAnnealingPeers.simulatedAnnealingPeers_AndMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        elif (method == "or"):
            bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = simulatedAnnealingPeers.simulatedAnnealingPeers_OrMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        elif (method == "numbers"):
            bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = simulatedAnnealingPeers.simulatedAnnealingPeers_NumbersMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        else:
            print("error_peers")
    elif (relationship == "groups"):
        if (method == "and"):
            bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = simulatedAnnealingGroups.simulatedAnnealingGroups_AndMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        elif (method == "or"):
            bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = simulatedAnnealingGroups.simulatedAnnealingGroups_OrMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        elif (method == "numbers"):
            bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = simulatedAnnealingGroups.simulatedAnnealingGroups_NumbersMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        else:
            print("error_groups")
    elif (relationship == "colours"):
        if (method == "and"):
            bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = simulatedAnnealingColours.simulatedAnnealingColours_AndMethod(dcel, r, tIni, tFin, l, n, minR, maxR, coloursDistribution, static)
        elif (method == "or"):
            bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = simulatedAnnealingColours.simulatedAnnealingColours_OrMethod(dcel, r, tIni, tFin, l, n, minR, maxR, coloursDistribution, static)
        elif (method == "numbers"):
            bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = simulatedAnnealingColours.simulatedAnnealingColours_NumbersMethod(dcel, r, tIni, tFin, l, n, minR, maxR, coloursDistribution, static)
        else:
            print("error_colours")
    else:
        print("error")    
    

    #managing name
    change = ""
    if (relationship != ""):
        relationship = ' - ' + relationship
    if (method != ""):
        method = ' - ' + method
    if (coloursDistribution != ""):
        coloursDistribution = ' - ' + coloursDistribution
        if (static):
            change = "- static"
        else:
            change = "- dynamic"
    
    
    #Final plot
    plottingModule.plt.figure(6+it)
    bestPVor = Voronoi(bestPSet)
    polygonsPBest = finiteVoronoi.vorFiniteDelPolygonsList(bestPVor, dcel.box)
    plottingModule.plotDcel(dcel, 'k')
    plottingModule.plt.suptitle('l: ' + repr(l) + ' - r: ' + repr(r))
    plottingModule.plt.title('SA' + relationship + method + coloursDistribution + change + " - best SD: " + repr(bestSD))
    plottingModule.plotPolys(polygonsPBest,'g')
    plottingModule.plotPoints(bestPSet,'-ob')
    
    plottingModule.plt.savefig(path + repr(bestSD) + '.jpg')
    
    return bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance
    
