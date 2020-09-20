"""
@author: cedelasen
"""

import data
import datetime
import easydict
import glob
import csv
import json
import pandas
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import finiteVoronoi
import plottingModule
import math
from scipy.spatial import (
    Voronoi,
    voronoi_plot_2d
)
import pickle

def process_args():

  args = easydict.EasyDict({
          "relationship": "classic",
          "method": "",
          "colourDistribution": "",
          "static": True
  })
  
  return args

def standardDeviation(results, mean):

  acc = 0
  n = len(results)

  for res in results:
    acc = acc + (res-mean)**2

  return math.sqrt(acc/n)

def meanData(csvPath):

    colnames = ["relationship","method","colourDistribution","static","l","r","maxExecsPS","result","p_acc","p_den","time"]
    data = pandas.read_csv(csvPath+'result.csv', names=colnames)

    l_set = list(set(data.l.tolist()[1:]))
    r_set = list(set(data.r.tolist()[1:]))
    execPS_set = list(set(data.maxExecsPS.tolist()[1:]))

    to_save = []

    print("PS\tl\tr\tmean")
    for execPS_i in execPS_set:
      print(execPS_i)
      for r_i in r_set:
        print("\t"+r_i)
        for l_i in l_set:
          print("\t\t"+l_i)
          with open(csvPath+'result.csv') as read_file:
            reader = csv.DictReader(read_file)

            accResults = 0
            results = []
            accTime = 0
            acc_p_acc = 0
            acc_p_den = 0
            cont = 0

            for row in reader:
              execPS = int(row['maxExecsPS'])
              r = float(row['r'])
              l = float(row['l'])
              result = float(row['result'])
              p_acc = float(row['p_acc'])
              p_den = float(row['p_den'])
              time = float(row['time'])

              check_execs = (int(execPS_i)==execPS)
              check_r = (float(r_i)==r)
              check_l = (float(l_i)==l)

              # print("\t\t\t"+str(check_execs))
              # print("\t\t\t"+str(check_r))
              # print("\t\t\t"+str(check_l))
              # print("\t\t\t\t"+str(execPS),str(r),str(l),str(result),str(time))

              if check_execs and check_r and check_l:
                #print("\t\t\t\t IN")
                accResults+=result
                results.append(result)
                accTime+=time
                acc_p_acc+=p_acc
                acc_p_den+=p_den
                cont+=1

              #print("\t\t\t"+"-----------------------------------------------")

            if not cont == 0:
              mean = str(round(accResults/cont, 6))
              sDev = str(round(standardDeviation(results, accResults/cont), 6))
              mean_time = str(datetime.timedelta(seconds=accTime/cont))
              acc = str(round(acc_p_acc/cont, 3))
              den = str(round(acc_p_den/cont, 3))
              n = str(cont)
              print("\t\t\tmean of results: " + mean + " (sD)")
              print("\t\t\tstandard deviation: " + sDev )
              print("\t\t\tmean time: " + mean_time + " (hh/mm/ss)")
              print("\t\t\tmean acc/den: " + acc + " (%) / " + den + " (%)")
              print("\t\t\tn: " + n )
              res=[execPS_i,r_i,l_i,mean,sDev,mean_time,acc,den,n]
              to_save.append(res)
              #print(res)

    if os.path.exists(csvPath+'result_resume.csv'):
      os.remove(csvPath+'result_resume.csv')

    with open(csvPath+'result_resume.csv','a') as f:
          fnames = ['PS','r','l','result','sDev','time','acc','den','n']
          writer = csv.DictWriter(f, fieldnames=fnames)
          writer.writeheader() #new file
          for res in to_save:
            writer.writerow({
              'PS':res[0],
              'r':res[1],
              'l':res[2],
              'result':res[3],
              'sDev':res[4],
              'time':res[5],
              'acc':res[6],
              'den':res[7],
              'n':res[8]
            })


def stochasticProcess(csvFiles, csvResultPath, jsonFiles):

    #dcel
    if os.path.exists("out/dcel_pS"):
      with open("out/dcel_pS", "rb") as read_file:
        dcel = pickle.load(read_file)
      read_file.close()  

    for (file, json_f) in zip( sorted(csvFiles),sorted(jsonFiles) ):
      cont=0
      its = []
      sDs = []
      bestsDs = []
      title = ""

      #csv
      with open(file) as read_file:
        reader = csv.DictReader(read_file)
        for row in reader:
          sDs.append(float(row['sd']))
          bestsDs.append(float(row['bestsd']))
          its.append(cont)
          cont+=1
      read_file.close()

      #csv result
      with open(csvResultPath) as read_file:
        reader = csv.DictReader(read_file)
        for row in reader:
          if row['result'] == str(bestsDs[-1]):

            title = title + row['relationship']

            if row['method'] != "":
              title = title + ", " + row['method']

            if row['colourDistribution'] != "":
              title = title + ", " + row['colourDistribution'] + ", " + row['static']

            #title = title + "\n"

            title = title + ", " + "l:" + row['l']
            title = title + ", " + "r:" + row['r']
            title = title + ", " + "execsPS:" + row['maxExecsPS']
            title = title + ", " + "acc: " + str(round(float(row['p_acc']),4)) + "%"
            title = title + ", " + "den: " + str(round(float(row['p_den']),4)) + "%"
            title = title + ", " + "time: " + str(datetime.timedelta(seconds=float(row['time'])))

            #title = title + "\n"

            title = title + ", " + "sd:" + row['result']             

            break

      read_file.close()

      #json
      with open(json_f) as read_file:
        p_set = json.load(read_file)
      read_file.close()
      #processing data json
      vor = Voronoi(p_set)
      polygons = finiteVoronoi.vorFiniteDelPolygonsList(vor, dcel.box)

      #plot
      with plt.rc_context(rc={'figure.max_open_warning': 0}):
        fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(14,5))
        fig.suptitle(title)

        ax1.plot(its,sDs, 'b')
        ax1.plot(its,bestsDs, 'r')
        ax1.set_title('stochastic process')
        ax1.set(xlabel='iteration', ylabel='symmetric difference')

        #ax2.set_axis_off()
        ax2.plot()
        plottingModule.plotDcel(dcel, 'k')
        plottingModule.plotPolys(polygons,'g')
        plottingModule.plotPoints(p_set,'-ob')
        ax2.set_title("symmetric difference: " + str(bestsDs[-1]))


def resumeResults():
    
    args = process_args()

    if (args.colourDistribution==''):
        if (args.relationship == 'classic'):
            path = args.relationship + "/"
        else:
            path = args.relationship + "/" + args.method + "/"
    else:
        path = args.relationship + "/" + args.method + "/" + args.colourDistribution + "/" + str(args.static) + "/"

    print("Resume of results -- " + path[:-1])
    print()

    #paths to load results
    csvPath = "out/csv/" + path
    csvResultPath = "out/csv/" + path + "result.csv"
    jsonPath = "out/json/" + path
    csvFiles = glob.glob(csvPath+"0*.csv")
    jsonFiles = glob.glob(jsonPath+"0*.json")

    meanData(csvPath)
    stochasticProcess(csvFiles,csvResultPath,jsonFiles)
