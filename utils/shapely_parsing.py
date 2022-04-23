# shapely_parsing.py

from sverchok.data_structure import get_edge_loop

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
                temp_edge_list = offset(temp_edge_list, idx)
            idx += N
            edge_list.extend(temp_edge_list)
    return edge_list