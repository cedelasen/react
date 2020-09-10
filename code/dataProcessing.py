"""
@author: cedelasen
"""

import data
import datetime
import easydict
import glob
import csv
import json
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

    with open(csvPath+'result.csv') as read_file:
      reader = csv.DictReader(read_file)
      accResults = 0
      accTime = 0
      cont=0

      for row in reader:
          result = float(row['result'])
          time = float(row['time'])
          accResults+=result
          accTime+=time
          cont+=1

    print("mean of results: " + str(accResults/cont) + " (sD)")
    print("mean time: " + str(datetime.timedelta(seconds=accTime/cont)) + " (hh/mm/ss)")
    
def schotasticProcess(csvFiles, imgFiles):

    for (file, img) in zip(csvFiles, imgFiles):
      print(file,img)
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

    #paths to load results
    csvPath = "out/csv/" + path
    imgPath = "out/results/" + path
    csvFiles = glob.glob(csvPath+"0*.csv")
    imgFiles = glob.glob(imgPath+"0*.jpg")

    print("Args: " + path.replace("/", ","))
    meanData(csvPath)
    schotasticProcess(csvFiles,imgFiles)
