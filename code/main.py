"""
@author: cedelasen
"""

import execution
import data
import plottingModule
import plantingSeeds
import finiteVoronoi
import dcelInstance
import psutil
import time
import argparse
import easydict
import csv
import json
import os
from scipy.spatial import (
    Voronoi,
    voronoi_plot_2d
)
import pickle

def process_args():

  args = easydict.EasyDict({
          "i": 10,
          "l": 0.06,
          "r": 0.095,
          "maxExecs": 5,
          "minR": 0,
          "maxR": 1,
          "relationship": "groups",
          "method": "numbers",
          "colourDistribution": "",
          "static": True
  })
  
  return args


def pre_execute(maxExecs, relationship, coloursDistribution):

    #ORIGINAL PARTITION to DCEL INSTANCE
    dcel = dcelInstance.dcelInstanceByVerticesEdges(data.vL, data.eL, data.iniX_palop, data.finX_palop, data.iniY_palop, data.finY_palop, data.finX_palop, data.finY_palop)

    #REMOVE EXTERNAL FACES
    for f in dcel.faces: #delete external face from list of dcel's faces
        if f.external:
            dcel.faces.remove(f)
        
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

    #initial voronoi diagram
    vor = Voronoi(pSetPlantingSeedsFin) #calculate voronoi
    
    ##polygons
    polygons = finiteVoronoi.vorFinitePolygonsList(vor) #vor to finiteVoronoi(polygons)

    if (relationship == "colours"):
        plantingSeeds.distroPoints(dcel, coloursDistribution)
        #Checking colours.
        plottingModule.plt.figure(5)
        plottingModule.plotDcel(dcel, 'k') #plot partition dcel instance
        plottingModule.plt.title('Checking colours' )
        plottingModule.plotPoints(pSetPlantingSeedsFin, '-ob')
        for f in dcel.faces:
            plottingModule.plt.plot(f.point[0], f.point[1], f.color)
        #save points 
    #save points 
        #save points 
        with open("out/dcel_pS_c", "wb") as write_file: #colored
          pickle.dump(dcel, write_file)
        write_file.close()
        with open("out/polygons_pS_c", "wb") as write_file:
          pickle.dump(polygons, write_file)
        write_file.close()
    else:
        #save points 
        with open("out/dcel_pS", "wb") as write_file: #not colored
          pickle.dump(dcel, write_file)
        write_file.close()
        with open("out/polygons_pS", "wb") as write_file:
          pickle.dump(polygons, write_file)
        write_file.close()

    return dcel, polygons


def execute(args):

  if (args.colourDistribution==''):
    path = args.relationship + "/" + args.method + "/"
  else:
    path = args.relationship + "/" + args.method + "/" + args.colourDistribution + "/" + str(args.static) + "/"


  #paths to store results
  imagePath = "out/results/" + path
  csvPath = "out/csv/" + path
  jsonPath = "out/json/" + path
      
  for i in range(args.i):
                  
      if (args.relationship == "colours"):
        if os.path.exists("out/dcel_pS_c") and os.path.exists("out/polygons_pS_c"):
          with open("out/dcel_pS_c", "rb") as read_file:
            dcel = pickle.load(read_file)
          read_file.close()
          with open("out/polygons_pS_c", "rb") as read_file:
            polygons = pickle.load(read_file)
          read_file.close()
        else:
          dcel, polygons = pre_execute(args.maxExecs, args.relationship, args.colourDistribution)
      else:
        if os.path.exists("out/dcel_pS") and os.path.exists("out/polygons_pS"):
          with open("out/dcel_pS", "rb") as read_file:
            dcel = pickle.load(read_file)
          read_file.close()
          with open("out/polygons_pS", "rb") as read_file:
            polygons = pickle.load(read_file)
          read_file.close()
        else:
          dcel, polygons = pre_execute(args.maxExecs, args.relationship, args.colourDistribution)


      start = time.time()

      bestPSet, bestSD, bestsDs, sDs, temps, its, acceptance = execution.execute(dcel, polygons, args.l, args.r, args.maxExecs, args.minR, args.maxR, args.relationship, args.method, args.colourDistribution, args.static, imagePath, i)
    
      end = time.time()
    
      print("\t\texecution nº:" + str(i) + " finished")
      accepted = acceptance.count(1)
      denied = acceptance.count(0)
      
      #save results
      with open(csvPath+'result.csv','a') as f:
            fnames = ['relationship','method','colourDistribution','static','l','r','maxExecsPS','result','p_acc','p_den','time']
            writer = csv.DictWriter(f, fieldnames=fnames)
            #writer.writeheader() #new file
            writer.writerow({'relationship' : args.relationship,
                            'method' : args.method,
                            'colourDistribution' : args.colourDistribution,
                            'static' : str(args.static),
                            'l' : str(args.l),
                            'r' : str(args.r),
                            'maxExecsPS' : str(args.maxExecs),
                            'result': str(bestSD),
                            'p_acc': str(accepted/(accepted+denied)),
                            'p_den': str(denied/(accepted+denied)),
                            'time': str(end - start)
                            })
      with open(csvPath+str(bestSD)+".csv",'a') as f:
            fnames = ['temp','it','bestsd','sd','acc']
            writer = csv.DictWriter(f, fieldnames=fnames)
            writer.writeheader() 
            for temp,it,bestsd,sd,acc in zip(temps,its,bestsDs,sDs,acceptance):
                writer.writerow({'temp': str(temp),'it': str(it),'bestsd': str(bestsd),'sd': str(sd),'acc': str(acc)})

      #save points 
      with open(jsonPath+str(bestSD)+".json", "w") as write_file:
            json.dump(bestPSet, write_file, indent=4)
              


def main():
  args = process_args()
  execute(args)
  
main()
