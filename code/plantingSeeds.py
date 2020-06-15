"""
@author: cedelasen
"""

import numpy
import plottingModule
import toolsModule
from shapely.geometry import (
    Polygon
)



def distroPoints(dcel, mode):

    """ set the color of the random points generated in pS' (planting seeds) method. """

    finX = dcel.box.bounds[2]
    finY = dcel.box.bounds[3]

    if mode == "random2colours":
        for f in dcel.faces:
            rand = numpy.random.uniform(0,1)
            if (rand<0.5):
                f.color = '-or'
            else:
                f.color = '-ob'
    elif mode == "4rectangles":
        for f in dcel.faces:
            p = f.point
            if p[0]<finX/2:
                if p[1]<finY/2:
                    f.color = '-or'
                else:#>=216
                    f.color = '-ob'
            else:#>=10
                if p[1]<finY/2:
                    f.color = '-ob'
                else:#>=216
                    f.color = '-or'
    elif mode == "16rectangles":
        for f in dcel.faces:
            p = f.point
            if (0<=p[0]<finX/4) or (finX/2<=p[0]<3*finX/4):
                if (0<=p[1]<finY/4) or (finY/2<=p[1]<3*finY/4):
                    f.color = '-or'
                else:
                    f.color = '-ob'
            else:
                if (0<=p[1]<finY/4) or (finY/2<=p[1]<3*finY/4):
                    f.color = '-ob'
                else:
                    f.color = '-or'
    elif mode == "random8colours":
        for f in dcel.faces:
            rand = numpy.random.uniform(0,1)
            if (rand<=0.125):
                f.color = '-ob'
            elif (rand<=0.25):
                f.color = '-og'
            elif (rand<=0.375):
                f.color = '-or'
            elif (rand<=0.5):
                f.color = '-oc'
            elif (rand<=0.625):
                f.color = '-om'
            elif (rand<=0.75):
                f.color = '-oy'
            elif (rand<=0.875):
                f.color = '-ok'
            else:
                f.color = '-ow'


def pS(dcel):
    
    """ planting seeds of the dcel given """
    
    file = open("tmp/initial_planting_seeds_log.txt","w") 
    file.flush
    
    print("Ejecutando PLANTING SEEDS")
    
    iniX = dcel.box.bounds[0]
    finX = dcel.box.bounds[2]
    iniY = dcel.box.bounds[1]
    finY = dcel.box.bounds[3]
    
    noValidos = 0
    cont = 0                                                #num figure counter
    
    
    for f in dcel.faces:                               #for each face
        
        file.write("NEW FACE. Num: "+ str(cont+1)+'\n')
        
        file.write("External? : "+ str(f.external)+'\n')
        
        file.write("-- VERTICES: "+'\n')
        fVL = f.coordsList()
        n = len(fVL)
        for i in range(0, n):
                file.write("--- ,"+' '+str(fVL[i][0])+' '+str(fVL[i][1])+'\n')

        polygons = []                                       #symmetric polygons list
        w = f.wedge                                         #take face's incident edge 
        nEdges = f.numEdges()                               #count num of edges/vertices (same number)
        
        for i in range(0, nEdges):                          #for each face's edge
            file.write("----- NEW EDGE. Num: "+ str(i+1)+'\n')
            p1 = [w.origin.x, w.origin.y]                   #save p1, segment point with which calculate symmetric points
            p2 = [w.twin.origin.x, w.twin.origin.y]         #save p2, segment point with which calculate symmetric points
            faceWedge = w.twin.face                         #symmetric hedge
            if not faceWedge.external:                      #if faceWedge not external
                cL = faceWedge.coordsList()                     #coords list
                n = len(cL)                                     #symmetric points number
                file.write("--------- COORDS LIST: "+'\n')
    
                for i in range(0, n):
                    file.write("-------------------------- ,"+' '+str(cL[i][0])+' '+str(cL[i][1])+'\n')
                    
                if not toolsModule.isValid(faceWedge, iniX, finX, iniY, finY):
                    file.write("-------------------------- External edge. Not useful"+'\n')#not using external face
                else:
                    poly=[]                                     #to store symmetric polygon coords
                    for i in range(0, n):                   
                        poly.append(
                                toolsModule.simmetricPoint(cL[i], p1, p2))#add new symmetric points to poly(gon)
                    file.write("--------- SYM COORDS LIST: "+'\n')    
                    for i in range(0, len(poly)):
                        file.write("-------------------------- ,"+' '+str(poly[i][0])+' '+str(poly[i][1])+'\n')
                    polygon = Polygon(poly)                     #compute polygon with the symmetric points
                    file.write("---------------------------- Validity: "+ str(polygon.is_valid)+'\n')
                    polygons.append(polygon)                    #store polygon
                
            w = w.nexthedge                                 #next edge
        
        cont = cont + 1

        inters = polygons[0]
        for p in range(1, len(polygons)):
            inters = inters.intersection(polygons[p])
        
        file.write("------------------------------------------- INTERSECTION RESULT type: "+ str(inters.type)+'\n')
        
        if (inters.type == 'Polygon' and inters):
            f.check = True
            f.polygon = inters
            plottingModule.plotPoly(f.polygon, 'b')
        else:
            f.check = False
            noValidos = noValidos + 1
            f.polygon = Polygon(f.coordsList())
            plottingModule.plotPoly(f.polygon, 'r')                                                     
        
    
        p_aux = f.polygon.centroid
        point = [p_aux.x,p_aux.y]
        f.point = point
        plottingModule.plotPoints([f.point], '-om')

    
    file.close
    
    return noValidos


def pScont(dcel, noValidos, maxExecs):
    
    """ cont. planting seeds of the partition given """


    file = open("tmp/initial_planting_seeds_cont_log.txt","w") 
    file.flush
    
    print("Ejecutando PLANTING SEEDS CONT")
    
    iniX = dcel.box.bounds[0]
    finX = dcel.box.bounds[2]
    iniY = dcel.box.bounds[1]
    finY = dcel.box.bounds[3]
    
    for execution in range(0,maxExecs): #execs of plantingSeedsCont algorithm
        file.write("EXEC. Num: "+ str(execution+1)+'\n')
        cont = 0
                                            
        for f in dcel.faces:
            file.write("NEW FACE. Num: "+ str(cont+1)+'\n')
            
            file.write("External? : "+ str(f.external)+'\n')
            
            file.write("-- VERTICES: "+'\n')
            
            fVL = f.coordsList()
            n = len(fVL)
            for i in range(0, n):
                file.write("--- ,"+' '+str(fVL[i][0])+' '+str(fVL[i][1])+'\n')
            
            if f.check:
                file.write("-- CHECK: TRUE "+'\n')
                w = f.wedge                    
                nEdges = f.numEdges()
                symetrics = []

                for n in range(0,nEdges):
                    p1 = [w.origin.x, w.origin.y]                                       #save p1, segment point with which calculate symmetric points
                    p2 = [w.twin.origin.x, w.twin.origin.y]                             #save p2, segment point with which calculate symmetric points
                    faceWedge = w.twin.face                                             #get twin face
                    if not faceWedge.external:                                          #if faceWedge not external
                        if toolsModule.isValid(faceWedge, iniX, finX, iniY, finY):
                            symetric = []                     
                            extracted = faceWedge.polygon                    
                            if extracted is not None:
                                coordsList = extracted.exterior.coords                      #coords of the polygon
                                for cL in coordsList:
                                    symetric.append(toolsModule.simmetricPoint(cL, p1, p2))          #calculate symmetric points
                                file.write("--------- SYM COORDS LIST: "+'\n')
                                for i in range(0, len(symetric)):
                                    file.write("-------------------------- ,"+' '+str(symetric[i][0])+' '+str(symetric[i][1])+'\n')
                                
                                polygon = Polygon(symetric) 
                                file.write("---------------------------- Validity: "+ str(polygon.is_valid)+'\n')
                                symetrics.append(polygon)
                    else:
                        file.write("-------------------------- External edge. Not useful"+'\n')
                        
                    w = w.nexthedge
                        
                        
                inters = symetrics[0]
                for i in range (1, len(symetrics)):                                     #intersect all symetrics
                    inters = inters.intersection(symetrics[i])
                file.write("------------------------------------------- INTERSECTION RESULT type: "+ str(inters.type)+'\n')
                
                if (inters.type == 'Polygon' and inters):
                    f.polygon = inters
                    plottingModule.plotPoly(f.polygon, 'b')
                    p_aux = f.polygon.centroid
                    point = [p_aux.x,p_aux.y]
                    f.point = point
                else:
                    f.check = False
                    noValidos = noValidos + 1
                    plottingModule.plotPoly(f.polygon, 'r')

                plottingModule.plotPoints([f.point], '-om')

            else:
                file.write("-- CHECK: FALSE "+'\n')
                
            cont = cont + 1
            
     


