"""
@author: cedelasen
"""

import execution_params as exec
import data_processing as dp
import datos as d
import plottingModule as pM
import dcelInstance as dI
import psutil as stats
import time
import argparse
import csv
import json

def process_args():
    
  parser = argparse.ArgumentParser(description='Execute (customized) simmulated annealing')

  parser.add_argument('-i',
                      dest='i',
                      type=int,
                      default=1,
                      help='num. of algorithm executions')
  
  parser.add_argument('-iniX',
                      dest='iniX',
                      type=float,
                      default=-50,
                      help='initial coord. X axis'
                      )

  parser.add_argument('-finX',
                      dest='finX',
                      type=float,
                      default=642,
                      help='final coord. X axis')
  
  parser.add_argument('-iniY',
                      dest='iniY',
                      type=float,
                      default=-50,
                      help='initial coord. Y axis'
                      )

  parser.add_argument('-finY',
                      dest='finY',
                      type=float,
                      default=464,
                      help='final coord. X axis')
  
  parser.add_argument('-l',
                      dest='l',
                      type=float,
                      default=0.06,
                      help='param to (re)calculate iterations in actual algorithm temperature, it = (t/l)*n')
  
  parser.add_argument('-r',
                      dest='r',
                      type=float,
                      default=0.095,
                      help='ratio to (re)calculate temperature, t = t*r')
  
  parser.add_argument('--maxExecs',
                      dest='maxExecs',
                      type=int,
                      default=1,
                      help='planting seeds cont. max. execs')
  
  parser.add_argument('--minR',
                      dest='minR',
                      type=float,
                      default=0,
                      help='uniform distribution min. random range value')
  
  parser.add_argument('--maxR',
                      dest='maxR',
                      type=float,
                      default=1,
                      help='uniform distribution max. random range value')
  
  parser.add_argument('--relationship',
                      dest='relationship',
                      type=str,
                      default='classic',
                      help='relationship between nodes')
  
  parser.add_argument('--method',
                      dest='method',
                      type=str,
                      default='',
                      help='association method between nodes')
  
  parser.add_argument('--colourDist',
                      dest='colourDistribution',
                      type=str,
                      default='',
                      help='nodes colours distribution')
  
  parser.add_argument('--static',
                      dest='static',
                      type=bool,
                      default=True,
                      help='nodes colours staticity')
  
  parsed_args = parser.parse_args()
  
  return parsed_args



def execute(args):

  if (args.colourDistribution==''):
    path = args.relationship + "/" + args.method + "/"
  else:
    path = args.relationship + "/" + args.method + "/" + args.colourDistribution + "/" + str(args.static) + "/"


  #paths to store results
  imagePath = "results/" + path
  csvPath = "csv/" + path
  jsonPath = "json/" + path
      
  for i in range(args.i):
      
      start = time.time()
      
      bestPSet, bestSD = exec.execute(args.iniX, args.finX, args.iniY, args.finY, args.l, args.r, args.maxExecs, args.minR, args.maxR, args.relationship, args.method, args.colourDistribution, args.static, imagePath)
    
      end = time.time()
    
      #save results
      with open(csvPath+'result.csv','a') as f:
          fnames = ['relationship','method','colourDistribution','static','l','r','maxExecsPS','result','time','tempC0','tempC1','tempC2','tempC3','tempC4','tempC5']
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
                          'time': str(end - start),
                          'tempC0': "/", #str(stats.sensors_temperatures()['coretemp'][1][1]),
                          'tempC1': "/", #str(stats.sensors_temperatures()['coretemp'][2][1]),
                          'tempC2': "/", #str(stats.sensors_temperatures()['coretemp'][3][1]),
                          'tempC3': "/", #str(stats.sensors_temperatures()['coretemp'][4][1]),
                          'tempC4': "/", #str(stats.sensors_temperatures()['coretemp'][5][1]),
                          'tempC5': "/"  #str(stats.sensors_temperatures()['coretemp'][6][1])
                          })
  
      #save points 
      with open(jsonPath+str(bestSD)+".json", "w") as write_file:
          json.dump(bestPSet, write_file, indent=4)
          


# def resumeResults(args):
    
#     if (args.colourDistribution==''):
#         if (args.relationship == 'classic'):
#             path = args.relationship + "/"
#         else:
#             path = args.relationship + "/" + args.method + "/"
#     else:
#         path = args.relationship + "/" + args.method + "/" + args.colourDistribution + "/" + str(args.static) + "/"

#     csvPath = "csv/" + path
    
#     # dp.resumeData(csvPath)



# def showResults(args):

#   if (args.colourDistribution==''):
#     path = args.relationship + "/" + args.method + "/"
#   else:
#     path = args.relationship + "/" + args.method + "/" + args.colourDistribution + "/" + str(args.static) + "/"

#   #paths to store results
#   #imagePath = "results/" + path
#   csvPath = "csv/" + path
#   jsonPath = "json/" + path
  
#   dcel = dI.generatorPointsToDcelInstance(d.gL, args.iniX, args.finX, args.iniY, args.finY, args.finX, args.finY)
#   for f in dcel.faces: #delete external face from list of dcel's faces
#     if f.external:
#       dcel.faces.remove(f)
  
#   pM.plotDcel(dcel, 'k')
  
#   data = dp.heatMap(csvPath, jsonPath)
#   for i in range(0,len(data)): 
#     pM.plotPoints(data[i], '-ob')
    
    
    

def main():
  args = process_args()
  execute(args)
  #resumeResults(args)
  #showResults(args)
  
  
main()
