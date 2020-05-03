#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#source: https://stackoverflow.com/questions/36063533/clipping-a-voronoi-diagram-python
#modified

import numpy as np
from shapely.geometry import Polygon

def vorFinitePolygons(vor, radius=None):
    
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0) #returns average on selected axis (in this case x axis)
    if radius is None:
        radius = vor.points.ptp().max()*2 #peak to peak (maximum-minimum).max

    # Construct a map containing all ridges for a given point #key
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))
        

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1] #access by key
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge
            t = vor.points[p2] - vor.points[p1] #tangent
            t /= np.linalg.norm(t)              #matriz de Frobenius
            n = np.array([-t[1], t[0]])         #normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)   


def vorFiniteDelPolygonsList(vor, min_x, max_x, min_y, max_y):
    
    """ returns a list of the voronoi's polygons delimited by min/max coords """ 
    
    regions, vertices = vorFinitePolygons(vor)

    mins = np.tile((min_x, min_y), (vertices.shape[0], 1))
    bounded_vertices = np.max((vertices, mins), axis=0)
    maxs = np.tile((max_x, max_y), (vertices.shape[0], 1))
    bounded_vertices = np.min((bounded_vertices, maxs), axis=0)

    box = Polygon([[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]])
    
    polygons = []

    for region in regions:
        
        polygon = vertices[region]
        poly = Polygon(polygon)
        poly = poly.intersection(box)
        if (poly.type == 'Polygon'):
            polygons.append(poly)
        
    return polygons

def vorFinitePolygonsList(vor):
    
    """ returns a list of the voronoi's polygons  """
    
    regions, vertices = vorFinitePolygons(vor)
    
    polygons = []
    
    for region in regions:
        
        polygon = vertices[region]
        poly = Polygon(polygon)
        polygons.append(poly)
    
    return polygons


    
    