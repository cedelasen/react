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


def process_args():

  args = easydict.EasyDict({
          "relationship": "classic",
          "method": "",
          "colourDistribution": "",
          "static": True
  })
  
  return args


def meanData(csvPath):

    colnames = ["relationship","method","colourDistribution","static","l","r","maxExecsPS","result","time"]
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
            accTime = 0
            cont = 0

            for row in reader:
              execPS = int(row['maxExecsPS'])
              r = float(row['r'])
              l = float(row['l'])
              result = float(row['result'])
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
                accTime+=time
                cont+=1

              #print("\t\t\t"+"-----------------------------------------------")

            print("\t\t\tmean of results: " + str(accResults/cont) + " (sD)")
            print("\t\t\tmean time: " + str(datetime.timedelta(seconds=accTime/cont)) + " (hh/mm/ss)")
            print("\t\t\tn: " + str(cont) )
            res=[execPS_i,r_i,l_i,str(accResults/cont),str(datetime.timedelta(seconds=accTime/cont)),str(cont)]
            to_save.append(res)
            #print(res)

    os.remove(csvPath+'result_resume.csv')

    with open(csvPath+'result_resume.csv','a') as f:
          fnames = ['PS','r','l','result','time','n']
          writer = csv.DictWriter(f, fieldnames=fnames)
          writer.writeheader() #new file
          for res in to_save:
            writer.writerow({
              'PS':res[0],
              'r':res[1],
              'l':res[2],
              'result':res[3],
              'time':res[4],
              'n':res[5]
            })


def stochasticProcess(csvFiles, imgFiles):

    for (file, img) in zip( sorted(csvFiles),sorted(imgFiles) ):
      cont=0
      its = []
      sDs = []
      bestsDs = [] 
      img_to_show = mpimg.imread(img)
      with open(file) as read_file:
        reader = csv.DictReader(read_file)
        for row in reader:
          sDs.append(float(row['sd']))
          bestsDs.append(float(row['bestsd']))
          its.append(cont)
          cont+=1
      fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(14,5))
      fig.suptitle("symmetric difference: " + str(bestsDs[-1]))
      ax2.set_axis_off()
      ax1.plot(its,sDs, 'b')
      ax1.plot(its,bestsDs, 'r')
      ax2.imshow(img_to_show)
      ax1.set_title('stochastic process')
      ax1.set(xlabel='iteration', ylabel='symmetric difference')
      ax2.set_title('voronoi calculated (green) and original partition (black)')


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
    imgPath = "out/results/" + path
    csvFiles = glob.glob(csvPath+"0*.csv")
    imgFiles = glob.glob(imgPath+"0*.jpg")

    meanData(csvPath)
    stochasticProcess(csvFiles,imgFiles)
