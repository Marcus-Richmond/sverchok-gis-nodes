
import copy
import numpy as np

import bpy
from bpy.props import BoolProperty


from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode
from sverchok.utils.dummy_nodes import add_dummy

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import clean_doubled_faces, triangle_mesh_viewer_map

if o3d is None:
    add_dummy('SvO3TriangleMeshCleanNode', 'Triangle Mesh Clean', 'open3d')
else:
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
import geopandas as gpd
import pandas as pd
import fiona
import numpy as np


class SvSGNImportGeometryPoint(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: GIS import
    Tooltip: Import GPKG point layer
    """
    bl_idname = 'SvSGNImportGeometryPoint'  # should be add to `sverchok/index.md` file
    bl_label = 'Import Point Geometry'
    bl_icon = 'RNA'

    def sv_init(self, context):  # All socket types are in `sverchok/core/sockets.py` file
        # inputs
        self.inputs.new('SvFilePathSocket', "GPKG Path")
        self.inputs.new('SvStringsSocket', "Layer Name")
        
        # outputs
        self.outputs.new('SvVerticesSocket', "Vertices")

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

            # determine how many dimensions are stored in coordinates
            coordinate_length = len(gi['features'][0]['geometry']['coordinates'])

            # for loop to create vertices
            if coordinate_length == 3:
                for feature in gi['features']:
                    x, y, z = feature['geometry']['coordinates']
                    Vertices_features_individual.append([x,y,z])
            elif coordinate_length == 2:
                for feature in gi['features']:
                    x, y = feature['geometry']['coordinates']
                    Vertices_features_individual.append([x,y,0])

            Vertices = [Vertices_features_individual]
            
            
        self.outputs["Vertices"].sv_set(Vertices)
        
        

def register():
        bpy.utils.register_class(SvSGNImportGeometryPoint)

def unregister():
        bpy.utils.unregister_class(SvSGNImportGeometryPoint)

def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshCleanNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshCleanNode)
