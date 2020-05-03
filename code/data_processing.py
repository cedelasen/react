#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 20:53:12 2019

@author: cxb0249
"""

import csv
import json
import plottingModule as pM
import dcelInstance as dI


csvPath = "csv/classic/"
jsonPath = "json/classic/"

axes = pM.plt.gca()
pM.plt.figure(1)

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
            #pM.plotPoints(data, '-ob')
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
    
    
    
