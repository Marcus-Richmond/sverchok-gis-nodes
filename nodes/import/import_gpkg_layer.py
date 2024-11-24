# This file is part of project Sverchok. It's copyrighted by the contributors
# recorded in the version control history of the file, available from
# its original location https://github.com/nortikin/sverchok/commit/master
#
# SPDX-License-Identifier: GPL3
# License-Filename: LICENSE


import bpy
from mathutils import Vector
from bpy.props import FloatProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok_gis.dependencies import geopandas as gpd
import numpy as np


class SvSGNImportGPKGLayer(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: gis import geopackage
    Tooltip: Import a layer from gpkg
    """
    bl_idname = 'SvSGNImportGPKGLayer' 
    bl_label = 'Import Geopackage Layer'
    bl_icon = 'GREASEPENCIL'

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvFilePathSocket', "GPKG Path")
        self.inputs.new('SvStringsSocket', "Layer Name")
        
        # outputs
        self.outputs.new('SvVerticesSocket', "Vertices")
        self.outputs.new('SvStringsSocket', "Edges")
        self.outputs.new('SvStringsSocket', "Polygons")
        self.outputs.new('SvStringsSocket', "Attributes")

    def process(self):
        # create initial variables for inputs 
        path = self.inputs["GPKG Path"].sv_get(deepcopy = False)
        layername = self.inputs["Layer Name"].sv_get(deepcopy = False)

        
        ##########################################################
        # ensure some kind of output even if nothing was found.
        # create empty lists to add output to
        list_of_lists_attributes = []
        list_of_lists_geometry = []
        list_polys = []
        list_edges = []
        
        if path:
            path = str(path[0][0])
        if layername:
            layername = str(layername[0][0])
            
        ##########################################################
        
            
        if path and layername:
            # read in gpkg layer as geopandas data frame, and make alias
            gdf = gpd.read_file(path, layer=layername).reset_index()
            
            # create dictionary of features in gdf to loop through
            dict_features = dict(iter(gdf.groupby('index')))

            # create empty lists to add output to
            list_of_lists_attributes = []
            list_of_lists_geometry = []

            # loop through dictionary of features
            for key_feature, value_feature in dict_features.items():
                # convert multipart geometries to singlepart
                df_singlepart = value_feature.explode(index_parts=True)
                
                # split parts into dict of dfs
                for key_part, value_part in dict(iter(df_singlepart.groupby(level=1))).items():
                    # get geometry type
                    geometry_type = value_part.geom_type.values[0]
                    
                    # if polygon, make geometry outer ring of polygon (i.e. remove inner rings, blender cannot handle rings in geometry the same way gis can)
                    if geometry_type == 'Polygon':
                        value_part.geometry = value_part.geometry.exterior
                        
                    # split parts into attributes / coordinates
                    part_attributes = value_part.drop(columns='geometry')
                    part_coordinates = value_part.get_coordinates(include_z=True, index_parts=True)
                    
                    # if z coordinate missing, fill in with 0
                    part_coordinates['z'].fillna(0, inplace=True)
                    
                    # create lists for edges and polygons
                    list_poly = part_coordinates.index.get_level_values(-1).tolist()
                    list_edge = [[item, item+1] for item in list_poly]
                    # change last vertex index to 0 in edges list, this will close line
                    # list_edge[-1] = [list_edge[-1][0], 0]
                    list_edge = list_edge[:-1]
                    
                    list_polys.append([list_poly])
                    list_edges.append(list_edge)
                    
                    # turn attributes and geometry into lists
                    list_attributes = part_attributes.values.tolist()
                    list_coords = part_coordinates.values.tolist()
                    
                    # append attribute and geometry lists to parent lists
                    list_of_lists_attributes.append(list_attributes)
                    list_of_lists_geometry.append(list_coords)
                


        # write output values
        self.outputs["Vertices"].sv_set(list_of_lists_geometry)
        self.outputs["Edges"].sv_set(list_edges)
        self.outputs["Polygons"].sv_set(list_polys)
        self.outputs["Attributes"].sv_set(list_of_lists_attributes)


def register():
    bpy.utils.register_class(SvSGNImportGPKGLayer)


def unregister():
    bpy.utils.unregister_class(SvSGNImportGPKGLayer)
