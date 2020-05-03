"""
@author: cedelasen
"""

import dcelInstance as dI
import datos as d
import plottingModule as pM
import plantingSeeds as pS
import simulatedAnnealing as sA_classic
import simulatedAnnealingPeers as sA_peers
import simulatedAnnealingGroups as sA_groups
import simulatedAnnealingColours as sA_colours
import finiteVor as fV
import symDif as sD
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Polygon
import math as m

    
def execute(iniX, finX, iniY, finY, l, r, maxExecs, minR, maxR, relationship, method, coloursDistribution, static, path):
 
    #BOUNDING BOX
    box = Polygon([[iniX, iniY], [iniX, finY], [finX, finY], [finX, iniY]])
    
    #ORIGINAL PARTITION to DCEL INSTANCE
    dcel = dI.generatorPointsToDcelInstance(d.gL, iniX, finX, iniY, finY, finX, finY)

    #REMOVE EXTERNAL FACES
    for f in dcel.faces:                                                            #delete external face from list of dcel's faces
        if f.external:
            dcel.faces.remove(f)
    
    #n
    n = len(dcel.faces)                                                         

    
    #planting seeds ini
    noValidos = pS.pS(dcel, iniX, finX, iniY, finY)
    pSetPlantingSeedsIni = dcel.points()
    
    #planting seeds fin
    pS.pScont(dcel, noValidos, maxExecs, iniX, finX, iniY, finY)
    pSetPlantingSeedsFin = dcel.points()
    
    #initial voronoi diagram
    vor = Voronoi(pSetPlantingSeedsFin)                                             #calculate voronoi
    
    ##polygons
    polygons = fV.vorFinitePolygonsList(vor)                                        #vor to finiteVor (polygons)
    
    
    #initial symmetric difference
    sd = sD.symDif(dcel, polygons, box)                                             #initial energy (global)
    
    #T inicial
    tIni = m.fabs(1/m.log10(sd))
    
    #T final
    tFin = tIni/(100*m.log10(n))
    
    #PARTITION CHECK
    pM.plt.figure(1)
    pM.plotDcel(dcel, 'k')                                                          #plot partition dcel instance
    pM.plt.title('DCEL partition check')
    
    ##PLANTING SEEDS
    pM.plt.figure(2)
    pM.plotDcel(dcel, 'k')                                                          #plot partition dcel instance
    pM.plt.title('Initial planting seeds')
    pM.plotPoints(pSetPlantingSeedsIni, '-og')                                     
    
    #PLANTING SEEDS cont.
    pM.plt.figure(3)
    pM.plotDcel(dcel, 'k')                                                          #plot partition dcel instance
    pM.plt.title('Planting seeds continuation ' + repr(maxExecs) + ' (it.)' )
    pM.plotPoints(pSetPlantingSeedsFin, '-ob')

    for f in dcel.faces:
        pM.plotPoly(f.polygon, 'c')
    
    
    ##VORONOI with post planting seeds points
    vor = Voronoi(pSetPlantingSeedsFin)
    voronoi_plot_2d(vor)
    pM.plt.show()
    
    #################################   SELECTOR   ##################################

    if (relationship == "colours"):
        pS.distroPoints(dcel, coloursDistribution, box.bounds[2], box.bounds[3])
        #Checking colours.
        pM.plt.figure(4)
        pM.plotDcel(dcel, 'k')                                                          #plot partition dcel instance
        pM.plt.title('Checking colours' )
        pM.plotPoints(pSetPlantingSeedsFin, '-ob')
        for f in dcel.faces:
            pM.plt.plot(f.point[0], f.point[1], f.color)
    
    #Execution switch
    if (relationship == "classic"):
        print("classic")
        bestPSet, bestSD, lastPSet, lastSD = sA_classic.simulatedAnnealing(dcel, pSetPlantingSeedsFin, vor, polygons, sd, r, tIni, tFin, l, n, minR, maxR, box)
    elif (relationship == "peers"):
        print("peers")
        if (method == "and"):
            print("and")
            bestPSet, bestSD, lastPSet, lastSD = sA_peers.simulatedAnnealingPeers_AndMethod(dcel, pSetPlantingSeedsFin, vor, polygons, sd, r, tIni, tFin, l, n, minR, maxR, box)
        elif (method == "or"):
            print("or")
            bestPSet, bestSD, lastPSet, lastSD = sA_peers.simulatedAnnealingPeers_OrMethod(dcel, pSetPlantingSeedsFin, vor, polygons, sd, r, tIni, tFin, l, n, minR, maxR, box)
        elif (method == "numbers"):
            print("numbers")
            bestPSet, bestSD, lastPSet, lastSD = sA_peers.simulatedAnnealingPeers_NumbersMethod(dcel, pSetPlantingSeedsFin, vor, polygons, sd, r, tIni, tFin, l, n, minR, maxR, box)
        else:
            print("error_peers")
    elif (relationship == "groups"):
        print("groups")
        if (method == "and"):
            print("and")
            bestPSet, bestSD, lastPSet, lastSD = sA_groups.simulatedAnnealingGroups_AndMethod(dcel, pSetPlantingSeedsFin, vor, polygons, sd, r, tIni, tFin, l, n, minR, maxR, box)
        elif (method == "or"):
            print("or")
            bestPSet, bestSD, lastPSet, lastSD = sA_groups.simulatedAnnealingGroups_OrMethod(dcel, pSetPlantingSeedsFin, vor, polygons, sd, r, tIni, tFin, l, n, minR, maxR, box)
        elif (method == "numbers"):
            print("numbers")
            bestPSet, bestSD, lastPSet, lastSD = sA_groups.simulatedAnnealingGroups_NumbersMethod(dcel, pSetPlantingSeedsFin, vor, polygons, sd, r, tIni, tFin, l, n, minR, maxR, box)
        else:
            print("error_groups")
    elif (relationship == "colours"):
        print("colours")
        if (method == "and"):
            print("and")
            bestPSet, bestSD, lastPSet, lastSD = sA_colours.simulatedAnnealingColours_AndMethod(dcel, pSetPlantingSeedsFin, vor, polygons, sd, r, tIni, tFin, l, n, minR, maxR, box, coloursDistribution, static)
        elif (method == "or"):
            print("or")
            bestPSet, bestSD, lastPSet, lastSD = sA_colours.simulatedAnnealingColours_OrMethod(dcel, pSetPlantingSeedsFin, vor, polygons, sd, r, tIni, tFin, l, n, minR, maxR, box, coloursDistribution, static)
        elif (method == "numbers"):
            print("numbers")
            bestPSet, bestSD, lastPSet, lastSD = sA_colours.simulatedAnnealingColours_NumbersMethod(dcel, pSetPlantingSeedsFin, vor, polygons, sd, r, tIni, tFin, l, n, minR, maxR, box, coloursDistribution, static)
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
    pM.plt.figure(5)
    bestPVor = Voronoi(bestPSet)
    polygonsPBest = fV.vorFiniteDelPolygonsList(bestPVor, iniX, finX, iniY, finY)
    pM.plotDcel(dcel, 'k')
    pM.plt.suptitle('l: ' + repr(l) + ' - r: ' + repr(r))
    pM.plt.title('SA' + relationship + method + coloursDistribution + change + " - best SD: " + repr(bestSD))
    pM.plotPolys(polygonsPBest,'g')
    pM.plotPoints(bestPSet,'-ob')
    
    
        
    pM.plt.savefig(path + repr(bestSD) + '.jpg')
    
    return bestPSet, bestSD
    
