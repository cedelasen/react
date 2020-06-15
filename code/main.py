"""
@author: cedelasen
"""

import execution
import data
import plottingModule
import dcelInstance
import psutil
import time
import argparse
import easydict
import csv
import json

def process_args():

  args = easydict.EasyDict({
          "i": 1,
          "l": 0.06,
          "r": 0.095,
          "maxExecs": 5,
          "minR": 0,
          "maxR": 1,
          "relationship": "colours",
          "method": "and",
          "colourDistribution": "4rectangles",
          "static": True
  })
  
  return args



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
      
      start = time.time()
      
      #execution.execute(args.l, args.r, args.maxExecs, args.minR, args.maxR, args.relationship, args.method, args.colourDistribution, args.static, imagePath)
      
      bestPSet, bestSD = execution.execute(args.l, args.r, args.maxExecs, args.minR, args.maxR, args.relationship, args.method, args.colourDistribution, args.static, imagePath)
    
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
                            'tempC0': "/", #str(psutil.sensors_temperatures()['coretemp'][1][1]),
                            'tempC1': "/", #str(psutil.sensors_temperatures()['coretemp'][2][1]),
                            'tempC2': "/", #str(psutil.sensors_temperatures()['coretemp'][3][1]),
                            'tempC3': "/", #str(psutil.sensors_temperatures()['coretemp'][4][1]),
                            'tempC4': "/", #str(psutil.sensors_temperatures()['coretemp'][5][1]),
                            'tempC5': "/"  #str(psutil.sensors_temperatures()['coretemp'][6][1])
                            })
          
        #save points 
      with open(jsonPath+str(bestSD)+".json", "w") as write_file:
            json.dump(bestPSet, write_file, indent=4)
              


def main():
  args = process_args()
  execute(args)
  
main()
