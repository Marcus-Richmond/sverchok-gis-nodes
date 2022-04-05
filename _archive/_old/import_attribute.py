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
from shapely.geometry import shape
import numpy as np


class SvScaleVectorNode(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: GIS import
    Tooltip: Import GPKG layer

    Merely for illustration of node creation workflow
    """
    bl_idname = 'SvScaleVectorNode'  # should be add to `sverchok/index.md` file
    bl_label = 'Custom Node'
    bl_icon = 'RNA'

    def sv_init(self, context):  # All socket types are in `sverchok/core/sockets.py` file
        self.inputs.new('SvFilePathSocket', "GPKG Path")
        self.inputs.new('SvStringsSocket', "Layer Name")
        self.inputs.new('SvStringsSocket', "Attribute Name")
        self.outputs.new('SvStringsSocket', "Path Out")
        self.outputs.new('SvStringsSocket', "Attribute")

    def process(self):        
        # filepath input/output test
        self.path = self.inputs["GPKG Path"].sv_get(deepcopy = False)
        
        self.outputs['Path Out'].sv_set(self.path)
        
        if self.path:
            # read in gpkg layer as geopandas data frame
            gpd1 = gpd.read_file(str(self.path[0][0]), layer = 'Locations_Points_CCC_v2')

            # call geo interface method on geodataframe
            gi = gpd1.__geo_interface__

            # variable to control which attribute is being extracted
            variableAttribute = '_Depth_Total'
            
            # create empty list to add attributes to
            listAttribute = []

            # loop through geointerface (gi) and extract values from the attribute, and add them to the list created above
            for features in range(len(gi['features'])):
                value = [gi['features'][features]['properties'][variableAttribute]]
                
                listAttribute.append(value)
            
            self.outputs["Attribute"].sv_set(listAttribute)
        
        
        

def register():
    bpy.utils.register_class(SvScaleVectorNode)