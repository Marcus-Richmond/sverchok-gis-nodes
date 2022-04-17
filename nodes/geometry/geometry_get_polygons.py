import bpy
import sverchok
import sverchok_gis
from sverchok.utils.dummy_nodes import add_dummy

from sverchok_gis.dependencies import geopandas as gpd

if gpd is None:
    add_dummy('SvSGNImportGeometryPolygon', 'load polygons', 'gpd')
else:

    from sverchok.node_tree import SverchCustomTreeNode
    from sverchok.data_structure import updateNode
    # import pandas as pd
    # import fiona
    # import numpy as np


    class SvSGNImportGeometryPolygon(SverchCustomTreeNode, bpy.types.Node):
        """
        Triggers: GIS import
        Tooltip: Import GPKG polygon layer
        """
        bl_idname = 'SvSGNImportGeometryPolygon'  # should be add to `sverchok/index.md` file
        bl_label = 'Import Polygon Geometry'
        bl_icon = 'RNA'

        def sv_init(self, context):  # All socket types are in `sverchok/core/sockets.py` file
            # inputs
            self.inputs.new('SvFilePathSocket', "GPKG Path")
            self.inputs.new('SvStringsSocket', "Layer Name")
            
            # outputs
            self.outputs.new('SvVerticesSocket', "Vertices")
            self.outputs.new('SvStringsSocket', 'Edges')
            self.outputs.new('SvStringsSocket', 'Polygons')

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
                coordinate_length = len(gi['features'][0]['geometry']['coordinates'][0][0])

                # for loop to create vertices
                for index in range(len(gi['features'])):
                    for index2 in range(len(gi['features'][index]['geometry']['coordinates'][0])-1):
                        
                        new_x = gi['features'][index]['geometry']['coordinates'][0][index2][0]
                        new_y = gi['features'][index]['geometry']['coordinates'][0][index2][1]
                        if coordinate_length == 3:
                            new_z = gi['features'][index]['geometry']['coordinates'][0][index2][2]
                        elif coordinate_length == 2:
                            new_z = 0
                        
                        new_vector = [new_x, new_y, new_z]

                        Vertices_features_individual.append(new_vector)
                    
                    Vertices_features_all.append(Vertices_features_individual)
                    
                    Vertices_features_individual = []

                Vertices = Vertices_features_all

                # create empty lists to add new edges and polygons to
                Edges_features_individual = []
                Edges_features_all = []
                Polygons_features_individual = []
                Polygons_features_all = []

                # for loop to create edges and polygons
                for index_edge in range(len(gi['features'])):
                    for index_edge2 in range(len(gi['features'][index_edge]['geometry']['coordinates'][0])-1):
                        
                        v1 = index_edge2
                        v2 = index_edge2 + 1

                        # if statement to reset v2 once it reaches the last vertex
                        if v2==len(gi['features'][index_edge]['geometry']['coordinates'][0])-1:
                            v2=0
                        
                        # create edge
                        e = (v1, v2)
                        
                        # append edge to edge list
                        Edges_features_individual.append(e)
                        
                        polygon_index = index_edge2
                        
                        # if statement to reset polygon index once it reaches the last vertex
                        if polygon_index == len(gi['features'][index_edge]['geometry']['coordinates'][0])-1:
                            polygon_index = 0
                        
                        Polygons_features_individual.append(polygon_index)
                    
                    Polygons_features_individual = [Polygons_features_individual]
                    
                    Edges_features_all.append(Edges_features_individual)
                    Polygons_features_all.append(Polygons_features_individual)
                    
                    Edges_features_individual = []
                    Polygons_features_individual = []

                Edges = Edges_features_all
                Polygons = Polygons_features_all
                
            self.outputs["Vertices"].sv_set(Vertices)
            self.outputs["Edges"].sv_set(Edges)
            self.outputs["Polygons"].sv_set(Polygons)
            
classes = [SvSGNImportGeometryPolygon]
register, unregister = sverchok_gis.utils.register_class_factory_deps(classes, deps=[gpd])            
            

# def register():
#     if gpd is not None:
#         bpy.utils.register_class(SvSGNImportGeometryPolygon)

# def unregister():
#     if gpd is not None:    
#         bpy.utils.unregister_class(SvSGNImportGeometryPolygon)

