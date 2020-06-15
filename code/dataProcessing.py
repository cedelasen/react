"""
@author: cedelasen
"""

import csv
import json
import plottingModule


csvPath = "out/csv/classic/"
jsonPath = "out/json/classic/"

axes = plottingModule.plt.gca()
plottingModule.plt.figure(1)

def process_args():

  args = easydict.EasyDict({
          "i": 1,
          "l": 0.06,
          "r": 0.095,
          "maxExecs": 5,
          "minR": 0,
          "maxR": 1,
          "relationship": "peers",
          "method": "numbers",
          "colourDistribution": "",
          "static": True
  })
  
  return args

def heatMap(csvPath,jsonPath):
  heatMap = []
  with open(csvPath+'result.csv') as read_file:
      reader = csv.DictReader(read_file)
      for row in reader:
          #print(row['result'])
          name = row['result']
          with open(jsonPath+name+".json", "r") as read_file:
            data = json.load(read_file)
            heatMap.append(data)
            #print(data)
            #print("--------------")
            #plottingModule.plotPoints(data, '-ob')
  return heatMap
         
data = heatMap(csvPath, jsonPath)

def resumeData(csvPath):
    with open(csvPath+'result.csv') as read_file:
      reader = csv.DictReader(read_file)
      cont = 0
      accResults = 0
      accTime = 0
      
      for row in reader:
          if cont < 80:
              result = float(row['result'])
              time = float(row['time'])
              accResults+=result
              accTime+=time
              #print(result)
              cont+=1
            
    print("mean of executions results: " + str(accResults/80))
    print("mean of execution times: " + str(accTime/80/60))
    
    
  
def resumeResults(args):
    
    if (args.colourDistribution==''):
        if (args.relationship == 'classic'):
            path = args.relationship + "/"
        else:
            path = args.relationship + "/" + args.method + "/"
    else:
        path = args.relationship + "/" + args.method + "/" + args.colourDistribution + "/" + str(args.static) + "/"

    csvPath = "csv/" + path
    
    resumeData(csvPath)



def showResults(args):

  if (args.colourDistribution==''):
    path = args.relationship + "/" + args.method + "/"
  else:
    path = args.relationship + "/" + args.method + "/" + args.colourDistribution + "/" + str(args.static) + "/"

  #paths to store results
  #imagePath = "results/" + path
  csvPath = "csv/" + path
  jsonPath = "json/" + path
  
  dcel = dcelInstance.dcelInstanceByGeneratorPoints(data.gL, args.iniX, args.finX, args.iniY, args.finY, args.finX, args.finY)
  for f in dcel.faces: #delete external face from list of dcel's faces
    if f.external:
      dcel.faces.remove(f)
  
  plottingModule.plotDcel(dcel, 'k')
  
  data = heatMap(csvPath, jsonPath)
  for i in range(0,len(data)): 
    plottingModule.plotPoints(data[i], '-ob')
    
    
def main():
  args = process_args()
  resumeResults(args)
  showResults(args)


main()
