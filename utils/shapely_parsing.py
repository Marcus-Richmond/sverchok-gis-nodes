# shapely_parsing.py
import mathutils
from sverchok.data_structure import get_edge_loop

def offset(inlist, n):
    return [[a+n, b+n] for a, b in inlist]


def get_edge_loops_from_multipoly(coords):
    """
    input:
        "coords" is a datatype similar to what you get from:

        coords = geo.__geo_interface__['coordinates']

    output:
        a list of edge indices that reference the vertices in coords as if they were a "flat" list of coordinate pairs.
        [[x1, y1], [x2, y2], ....]

    """

    idx = 0
    edge_list = []
    for coordset in coords:
        for loop in coordset:
            N = len(loop)
            temp_edge_list = get_edge_loop(N)
            if idx > 0:
                temp_edge_list = [[a+idx, b+idx] for a, b in temp_edge_list]
            idx += N
            edge_list.extend(temp_edge_list)
    return edge_list


def get_face_indices_from_multipoly(coords):
    """
    this is similar to get_edge_loops_from_multipoly, except it tesselates complex ngons and 
    returns their index lists.
    """
    idx = 0
    face_list = []
    for coordset in coords:
        for loop in coordset:
            N = len(loop)
            temp_face_list = mathutils.geometry.tessellate_polygon([loop])
            if idx > 0:
                temp_face_list = [[i+idx for i in a] for a in temp_face_list]
            idx += N
            face_list.extend(temp_face_list)
    return face_list 