import copy
import numpy as np

import bpy
from sverchok_gis.dependencies import geopandas as gpd
from sverchok.utils.dummy_nodes import add_dummy


if gpd is None:
    add_dummy('SvSGNImportGeometryLine', 'Get Line Geometry', 'geopandas')
else:
    # from mathutils import Vector
    # from bpy.props import FloatProperty
    from sverchok.node_tree import SverchCustomTreeNode
    from sverchok.data_structure import updateNode
    
    # -------------unless these are specifically used, they do not need to be imported. ------- #
    
    # import pandas as pd
    # import fiona
    # import numpy as np


    class SvSGNImportGeometryLine(SverchCustomTreeNode, bpy.types.Node):
        """
        Triggers: GIS import
        Tooltip: Import GPKG line layer
        """
        bl_idname = 'SvSGNImportGeometryLine'  # should be add to `sverchok/index.md` file
        bl_label = 'Import Line Geometry'
        bl_icon = 'RNA'

        def sv_init(self, context):  # All socket types are in `sverchok/core/sockets.py` file
            # inputs
            self.inputs.new('SvFilePathSocket', "GPKG Path")
            self.inputs.new('SvStringsSocket', "Layer Name")
            
            # outputs
            self.outputs.new('SvVerticesSocket', "Vertices")
            self.outputs.new('SvStringsSocket', 'Edges')

        def process(self):  
            # create initial variables      
            self.path = self.inputs["GPKG Path"].sv_get(deepcopy = False)
            self.layername = self.inputs["Layer Name"].sv_get(deepcopy = False)        
            
            if self.path and self.layername:
                self.layername = str(self.layername[0][0])

                # read in gpkg layer as geopandas data frame
                gpd1 = gpd.read_file(str(self.path[0][0]), layer = self.layername)

                # call geo interface method on geodataframe
                gi = gpd1.__geo_interface__

                # create empty lists to add new vertices to
                Vertices_features_individual = []
                Vertices_features_all = []

                # determine how many dimensions are stored in coordinates
                coordinate_length = len(gi['features'][0]['geometry']['coordinates'][0])

                # for loop to create vertices
                for index in range(len(gi['features'])):
                    for index2 in range(len(gi['features'][index]['geometry']['coordinates'])):
                        
                        new_x = gi['features'][index]['geometry']['coordinates'][index2][0]
                        new_y = gi['features'][index]['geometry']['coordinates'][index2][1]
                        if coordinate_length == 3:
                            new_z = gi['features'][index]['geometry']['coordinates'][index2][2]
                        elif coordinate_length == 2:
                            new_z = 0
                        
                        new_vector = [new_x, new_y, new_z]

                        Vertices_features_individual.append(new_vector)
                    
                    Vertices_features_all.append(Vertices_features_individual)
                    
                    Vertices_features_individual = []

                Vertices = Vertices_features_all

                # create empty lists to add new edges to
                Edges_features_individual = []
                Edges_features_all = []

                # for loop to create edges and polygons
                for index_edge in range(len(gi['features'])):
                    for index_edge2 in range(len(gi['features'][index_edge]['geometry']['coordinates'])-1):
                        
                        v1 = index_edge2
                        v2 = index_edge2 + 1
                        
                        # create edge
                        e = (v1, v2)
                        
                        # append edge to edge list
                        Edges_features_individual.append(e)
                    
                    Edges_features_all.append(Edges_features_individual)
                    
                    Edges_features_individual = []

                Edges = Edges_features_all
                
            self.outputs["Vertices"].sv_set(Vertices)
            self.outputs["Edges"].sv_set(Edges)      

"""
def sverchok.utils.registration_class_factory_deps(classes, deps=None):

    import bpy
    def register():
        if all in deps:
            _ = [bpy.utils.register_class(c) for c in classes]

    def unregister():
        if all in deps:
            _ = [bpy.utils.unregister_class(c) for c in classes]

    return register, unregister

classes = [SvSGNImportGeometryLine]
register, unregister = sverchok.utils.registration_class_factory_deps(classes, deps=[gpd])

"""

def register():
    if gpd is not None:
        bpy.utils.register_class(SvSGNImportGeometryLine)

def unregister():
    if gpd is not None:
        bpy.utils.unregister_class(SvSGNImportGeometryLine)
