#Copyright 2008, Angel Yanguas-Gil
#edited

import math
import random
import functools



class DcelError(Exception): pass



class Vertex:

    """Minimal implementation of a vertex of a 2D dcel"""

    def __init__(self, px, py):
        self.x = px
        self.y = py
        self.hedgelist = []

    def sortincident(self):
        self.hedgelist = sorted(self.hedgelist, key=functools.cmp_to_key(self.hsort), reverse=True)

    def hsort(self, h1, h2):

        """Sorts two half edges counterclockwise"""

        if h1.angle < h2.angle:
            return -1
        elif h1.angle > h2.angle:
            return 1
        else:
            return 0


class Hedge:

    """Minimal implementation of a half-edge of a 2D dcel"""

    def __init__(self,v1,v2):
        self.origin = v2                                                        #the origin is defined as the vertex it points to
        self.twin = None
        self.face = None
        self.nexthedge = None
        self.angle = self.hangle(v2.x-v1.x, v2.y-v1.y)
        self.prevhedge = None
        self.length = math.sqrt((v2.x-v1.x)**2 + (v2.y-v1.y)**2)

    def hangle(self,dx,dy):

        """Determines the angle with respect to the x axis of a segment
        of coordinates dx and dy
        """

        l = math.sqrt(dx*dx + dy*dy)
        if dy > 0:
            return math.acos(dx/l)
        else:
            return 2*math.pi - math.acos(dx/l)


class Face:

    """Implementation of a face of a 2D dcel"""

    def __init__(self):
        self.wedge = None                                                       #incident edge
        self.external = None
        self.polygon = None
        self.point = None
        self.color = None
        self.check = None

    def area(self):                                                             #Gauss's area formula - shoelace formula
        h = self.wedge
        a = 0
        while(not h.nexthedge is self.wedge):
            p1 = h.origin
            p2 = h.nexthedge.origin
            a += p1.x*p2.y - p2.x*p1.y
            h = h.nexthedge
            
        #close loop
        p1 = h.origin
        p2 = self.wedge.origin

        #last it. and symmetric difference
        a = (a + p1.x*p2.y - p2.x*p1.y)/2

        return a

    def perimeter(self): #module sum
        h = self.wedge
        p = 0
        while (not h.nexthedge is self.wedge):
            p += h.length
            h = h.nexthedge
        return p

    def vertexList(self): 
        h = self.wedge
        pl = [h.origin]
        while(not h.nexthedge is self.wedge):
            h = h.nexthedge
            pl.append(h.origin)
        return pl

    def coordsList(self):
        h = self.wedge
        pl = [[h.origin.x, h.origin.y]]
        while(not h.nexthedge is self.wedge):
            h = h.nexthedge
            pl.append([h.origin.x, h.origin.y])
        return pl

    def getWedge(self, i):
        w = self.wedge
        cont = 0
        while (cont == i):
            w = w.nexthedge
            cont += 1
        return w

    def numEdges(self):
        h = self.wedge
        cont = 1
        while(not h.nexthedge is self.wedge):
            h = h.nexthedge
            cont+= 1
        return cont

    def isInside(self, p):                                                      #determines if a point is inside a face
         
        h = self.wedge
        if self.leftOn(h, p):
            while(not h.nexthedge is self.wedge):
                h = h.nexthedge
                if not self.leftOn(h, p):
                    return False
            return True
        else:
            return False


    def leftOn(self, hedge, point):

        """Determines if a point is to the left of a hedge"""

        return self.crossProduct(hedge, point) >= 0


    def crossProduct(self, hedge, point):
        
        """Determines the 'oriented' area of the triangle formed by a hedge and
        an external point"""

        pa = hedge.twin.origin
        pb = hedge.origin
        pc = point
        return (pb.x - pa.x)*(pc[1] - pa.y) - (pc[0] - pa.x)*(pb.y - pa.y)


    def randomEdgeNotExt(self):                                                 #returns a random edge of edge (no composing the bounding box)
        
        #f = dcel.faces[random.randint(0,n-1)]                                  #upper select random face
        i = random.randint(0,self.numEdges()-1)                                      #random index in range (0-num of face's edges)
        w = self.getWedge(i)                                                    #index selected wedge
        
        while (w.twin.face.external):                                           #if not point (external) -> select the next not external edge
            w = w.nexthedge                                                     #best case: interior face
                                                                                #mid case: exterior face with only one external edge
                                                                                #worst case: exterior face with two external edges
        return w


class Dcel:

    """ Implements a doubly-connected edge list - DCEL """

    def __init__(self, vl=[], el=[], box=[]):
        self.vl = vl
        self.el = el
        self.box = box    
        self.vertices = []
        self.hedges = []
        self.faces = []
        
    def build_dcel(self):

        """ Creates the dcel from the list of vertices and edges """

        #Step 1: vertex list creation
        for v in self.vl:
            self.vertices.append(Vertex(v[0], v[1]))

        #Step 2: hedge list creation. Assignment of twins and
        #vertices
        for e in self.el:
            if e[0] >= 0 and e[1] >= 0:
                #tomo cada 'arista' del conjunto de aristas, que en realidad no 
                #es eso si no un par de index para el array de vértices
                #nos es muy útil de acuerdo con la partición artificial creada
                h1 = Hedge(self.vertices[e[0]], self.vertices[e[1]])
                h2 = Hedge(self.vertices[e[1]], self.vertices[e[0]])
                h1.twin = h2
                h2.twin = h1
                #recordamos que el origen es donde apunta la flecha
                #desde esta implementación de código
                self.vertices[e[1]].hedgelist.append(h1)
                self.vertices[e[0]].hedgelist.append(h2)
                self.hedges.append(h2)
                self.hedges.append(h1)

        #Step 3: Identification of next and prev hedges
        cont = 0
        for v in self.vertices:
            v.sortincident()
            l = len(v.hedgelist)
            cont = cont + 1
            if l < 2: 
               raise DcelError(
                    "Badly formed dcel: less than two hedges in vertex")                                                                                
            else:
                for i in range(l-1):
                    #itero todos las aristas comunes a un vértice
                    #accedo a la arista i y le digo que 
                    v.hedgelist[i].nexthedge = v.hedgelist[i+1].twin
                    v.hedgelist[i+1].prevhedge = v.hedgelist[i]
                v.hedgelist[l-1].nexthedge = v.hedgelist[0].twin
                v.hedgelist[0].prevhedge = v.hedgelist[l-1]

        #Step 4: Face assignment
        provlist = self.hedges[:]
        nf = 0
        nh = len(self.hedges)

        while nh > 0:
            h = provlist.pop()#extraigo
            nh -= 1
            if h.face == None: #check if the hedge already points to a face
                f = Face()
                nf += 1
                #We link the hedge to the new face
                f.wedge = h
                f.wedge.face = f
                #And we traverse the boundary of the new face
                while (not h.nexthedge is f.wedge):
                    h = h.nexthedge
                    h.face = f
                self.faces.append(f)
        #And finally we have to determine the external face
        for f in self.faces:
            f.external = f.area()<0

    def areas(self):
        return [f.area() for f in self.faces if not f.external]

    def perimeters(self):
        return [f.perimeter() for f in self.faces if not f.external]

    def nfaces(self):
        return len(self.faces)

    def nvertices(self):
        return len(self.vertices)

    def nedges(self):
        return len(self.hedges)/2

    def points(self):
        points = []
        for f in self.faces:
            points.append(f.point)
        return points


