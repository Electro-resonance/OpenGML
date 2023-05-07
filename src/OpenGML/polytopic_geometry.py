# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 30th April 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Helper functions to convert vertices into
# arrays of indexes representing edges and faces of regular and irregular polytope.
# Note that some of these functions are in development.
# =============================================================================


import numpy as np
import cdd as pcdd # Requires the pycddlib
import scipy.spatial
#rom scipy.spatial import Delaunay
#from scipy.spatial import HalfspaceIntersection

def point_list_to_array(point_list):
    # Prepend a column of ones as required by convex hull with cdd
    edges_list = []
    vertices=[]
    #if (vertice_count >= 6):
        #print(" point_list_to_array vertice count", vertice_count)
    points1 = np.array(point_list)
    array_shape=points1.shape
    #print("point list shape:", array_shape)
    if(len(array_shape)>1 and array_shape[1]==3):
        return points1
    vertice_count = int(points1.shape[0] / 3)
    #print(" point_list_to_array vertice count", points1.shape)
    vertices = points1.reshape(vertice_count, 3)
        #vertices = np.hstack((np.ones((vertice_count, 1)), points2))
        #print("point_list_to_array", vertices)
    return vertices

def remove_same_points(points,verbose=False):
    last_point=[-9990,-9990,-9990]
    new_points=[]
    for point in points:
        if(verbose==True):
            print("Last:",last_point," current:",point)
        if(last_point[0]==point[0] and last_point[1]==point[1] and last_point[2]==point[2]):
            if (verbose == True):
                print("Removal of: ", point)
            pass
        else:
            new_points.append(point)
        last_point=point
    return new_points

def pre_check_polytope(points,list_format=True,verbose=False):
    if (verbose==True):
        print("Start Points:", points)

    if (list_format==True):
        points2=point_list_to_array(points)
    else:
        point2=points

    if(len(points2)==0):
        if (verbose == True):
            print("Check - No points", points2)
        return [None,0]
    #print("Using points")

    if (verbose == True):
        print("Remove same")
    points3=remove_same_points(points2,verbose)

    vertice_count = int(len(points3))
    if (verbose==True):
        print("Vertice count post remove:", vertice_count, points3)
    if (vertice_count < 6):
        return [None,vertice_count]

    if (verbose==True):
        print("Process Points:", points)
    return [points3,vertice_count]

def vertices_to_edge_sequence(points, list_format=True, verbose=False):
    """
    Calculate the sequence of edges for a given list of vertices
    See: https://stackoverflow.com/questions/27270477/3d-convex-hull-from-point-cloud
    :param vertices:
    :return:
    """
    [points,vertice_count] = pre_check_polytope(points, list_format, verbose)
    if (points is None):
        return None

    # Prepend a column of ones as required by convex hull with cdd
    vertices = np.hstack((np.ones((vertice_count, 1)), points))

    # Perform the convex hull on the polyhedron
    mat = pcdd.Matrix(vertices, linear=False, number_type="fraction")
    mat.rep_type = pcdd.RepType.GENERATOR
    poly = pcdd.Polyhedron(mat)

    # Obtain the facets of the polyhedron as a list of lists of vertex indices
    facets_interim = poly.get_inequalities()
    if(verbose==True):
        print("facets:",facets_interim)

    facets=[]
    for facet in facets_interim:
        if(len(facet)>1):
            facets.append(facet[1:])

    adjacencies = [list(x) for x in poly.get_input_adjacency()]

    edges = []
    if(verbose==True):
        print("Adjacencies:",adjacencies)
    for i, indices in enumerate(adjacencies[:-1]):
        indices = list(filter(lambda x: x > i, indices))
        #indices = list(filter(lambda x: x > i and any(i in f and x in f for f in facets_interim), indices))
        l = len(indices)
        if (l > 0):
            col1 = np.full((l, 1), i)
            indices = np.reshape(indices, (l, 1))
            edges.append(np.hstack((col1, indices)))
    if (len(edges) > 0):
        edges_list = np.vstack(tuple(edges))
    if(verbose==True):
        print("Edges list:", edges_list)
    return edges_list

def basic_vertices_to_edge_sequence(points, list_format=True, verbose=False):
    """
    Calculate the sequence of edges for a given list of vertices
    See: https://stackoverflow.com/questions/27270477/3d-convex-hull-from-point-cloud
    :param vertices:
    :return:
    """
    [points,vertice_count] = pre_check_polytope(points, list_format, verbose=False)
    if (points is None):
        print("No points in basic_vertices_to_edge_sequence")
        return None
    # create a ConvexHull object from the vertices
    try:
        hull = scipy.spatial.ConvexHull(points, incremental=True)
        # # Get the indices of the vertices that form the facets of the hull
        facets = hull.simplices
    except Exception as e:
        print("Covex hull error: ",e)
        return None


    # create an empty list to store the vertices without diagonals
    vertices_no_diag = []
    # loop through each facet
    for facet in facets:
        vertices_facet=[]
        # loop through each pair of vertices in the facet
        for i in range(len(facet)):
            v1 = facet[i]
            v2 = facet[(i + 1) % len(facet)]

                # check if the pair of vertices is adjacent on the hull
                # add the pair of vertices to the list
            vertices_facet.append(sorted([v1, v2]))
        vertices_no_diag.append(vertices_facet)

            # check if the pair of vertices is not a diagonal
            #if any(v1 in f and v2 in f for f in facets if f is not facet):
            #   # add the pair of vertices to the list
            #    vertices_no_diag.append(sorted([v1, v2]))

    # convert the list to a numpy array
    vertices_no_diag = np.array(vertices_no_diag)

    if(verbose==True):
        # print the array of vertices without diagonals
        print("Basic poytope", vertices_no_diag, len(vertices_no_diag))
    return vertices_no_diag