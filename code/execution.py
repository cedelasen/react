"""
@author: cedelasen
"""

import dcelInstance
import data
import finiteVoronoi
import math
import plottingModule
import plantingSeeds
import simulatedAnnealing
import simulatedAnnealingPeers
import simulatedAnnealingGroups
import simulatedAnnealingColours
import symmetricDifference

from scipy.spatial import (
    Voronoi,
    voronoi_plot_2d
)

    
def execute(l, r, maxExecs, minR, maxR, relationship, method, coloursDistribution, static, path):
 
    
    #ORIGINAL PARTITION to DCEL INSTANCE
    dcel = dcelInstance.dcelInstanceByVerticesEdges(data.vL, data.eL, data.iniX_palop, data.finX_palop, data.iniY_palop, data.finY_palop, data.finX_palop, data.finY_palop)

    #REMOVE EXTERNAL FACES
    for f in dcel.faces: #delete external face from list of dcel's faces
        if f.external:
            dcel.faces.remove(f)
    
    #n
    n = len(dcel.faces)                                                         
    
    #PARTITION CHECK
    plottingModule.plt.figure(1)
    plottingModule.plotDcel(dcel, 'k') #plot partition dcel instance
    plottingModule.plt.title('DCEL partition check')

    ##PLANTING SEEDS
    plottingModule.plt.figure(2)
    plottingModule.plotDcel(dcel, 'k') #plot partition dcel instance
    plottingModule.plt.title('Initial planting seeds')

    #planting seeds ini
    noValidos = plantingSeeds.pS(dcel)
    pSetPlantingSeedsIni = dcel.points()
    plottingModule.plotPoints(pSetPlantingSeedsIni, '-ok')

    
    #PLANTING SEEDS cont.
    plottingModule.plt.figure(3)
    plottingModule.plotDcel(dcel, 'k') #plot partition dcel instance
    plottingModule.plt.title('Planting seeds continuation ' + repr(maxExecs) + ' (it.)' )
    
    #planting seeds fin
    plantingSeeds.pScont(dcel, noValidos, maxExecs)
    pSetPlantingSeedsFin = dcel.points()
    plottingModule.plotPoints(pSetPlantingSeedsFin, '-ok')    
    
    
    #initial voronoi diagram
    vor = Voronoi(pSetPlantingSeedsFin) #calculate voronoi
    
    ##polygons
    polygons = finiteVoronoi.vorFinitePolygonsList(vor) #vor to finiteVoronoi(polygons)
    
    
    #initial symmetric difference
    sd = symmetricDifference.symDif(dcel.faces, polygons, dcel.box) #initial energy (global)
    
    #T inicial
    tIni = math.fabs(1/math.log10(sd))
    
    #T final
    tFin = tIni/(100*math.log10(n))
    
    plottingModule.plt.figure(4)
    plottingModule.plotDcel(dcel, 'k') #plot partition dcel instance
    plottingModule.plt.title('Pre Simulated Annealing' )
    for f in dcel.faces:
        plottingModule.plotPoly(f.polygon, 'c')
    plottingModule.plotPoints(pSetPlantingSeedsFin, '-ok')    

    
    ##VORONOI with post planting seeds points
    vor = Voronoi(pSetPlantingSeedsFin)
    voronoi_plot_2d(vor)
    plottingModule.plt.show()
    
    #################################   SELECTOR   ##################################

    if (relationship == "colours"):
        plantingSeeds.distroPoints(dcel, coloursDistribution)
        #Checking colours.
        plottingModule.plt.figure(5)
        plottingModule.plotDcel(dcel, 'k') #plot partition dcel instance
        plottingModule.plt.title('Checking colours' )
        plottingModule.plotPoints(pSetPlantingSeedsFin, '-ob')
        for f in dcel.faces:
            plottingModule.plt.plot(f.point[0], f.point[1], f.color)
    
    #Execution switch
    if (relationship == "classic"):
        bestPSet, bestSD, bestsDs, sDs, temps, its = simulatedAnnealing.simulatedAnnealing(dcel, r, tIni, tFin, l, n, minR, maxR)
    elif (relationship == "peers"):
        if (method == "and"):
            bestPSet, bestSD, bestsDs, sDs, temps, its = simulatedAnnealingPeers.simulatedAnnealingPeers_AndMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        elif (method == "or"):
            bestPSet, bestSD, bestsDs, sDs, temps, its = simulatedAnnealingPeers.simulatedAnnealingPeers_OrMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        elif (method == "numbers"):
            bestPSet, bestSD, bestsDs, sDs, temps, its = simulatedAnnealingPeers.simulatedAnnealingPeers_NumbersMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        else:
            print("error_peers")
    elif (relationship == "groups"):
        if (method == "and"):
            bestPSet, bestSD, bestsDs, sDs, temps, its = simulatedAnnealingGroups.simulatedAnnealingGroups_AndMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        elif (method == "or"):
            bestPSet, bestSD, bestsDs, sDs, temps, its = simulatedAnnealingGroups.simulatedAnnealingGroups_OrMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        elif (method == "numbers"):
            bestPSet, bestSD, bestsDs, sDs, temps, its = simulatedAnnealingGroups.simulatedAnnealingGroups_NumbersMethod(dcel, r, tIni, tFin, l, n, minR, maxR)
        else:
            print("error_groups")
    elif (relationship == "colours"):
        if (method == "and"):
            bestPSet, bestSD, bestsDs, sDs, temps, its = simulatedAnnealingColours.simulatedAnnealingColours_AndMethod(dcel, r, tIni, tFin, l, n, minR, maxR, coloursDistribution, static)
        elif (method == "or"):
            bestPSet, bestSD, bestsDs, sDs, temps, its = simulatedAnnealingColours.simulatedAnnealingColours_OrMethod(dcel, r, tIni, tFin, l, n, minR, maxR, coloursDistribution, static)
        elif (method == "numbers"):
            bestPSet, bestSD, bestsDs, sDs, temps, its = simulatedAnnealingColours.simulatedAnnealingColours_NumbersMethod(dcel, r, tIni, tFin, l, n, minR, maxR, coloursDistribution, static)
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
    plottingModule.plt.figure(6)
    bestPVor = Voronoi(bestPSet)
    polygonsPBest = finiteVoronoi.vorFiniteDelPolygonsList(bestPVor, dcel.box)
    plottingModule.plotDcel(dcel, 'k')
    plottingModule.plt.suptitle('l: ' + repr(l) + ' - r: ' + repr(r))
    plottingModule.plt.title('SA' + relationship + method + coloursDistribution + change + " - best SD: " + repr(bestSD))
    plottingModule.plotPolys(polygonsPBest,'g')
    plottingModule.plotPoints(bestPSet,'-ob')
    
    plottingModule.plt.savefig(path + repr(bestSD) + '.jpg')
    
    return bestPSet, bestSD, bestsDs, sDs, temps, its
    
