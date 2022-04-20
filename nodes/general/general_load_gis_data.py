# general_load_gis_data.py

# This file is part of project Sverchok-gis. It's copyrighted by the contributors
# recorded in the version control history of the file, available from
# its original location https://github.com/Marcus-Richmond/sverchok-gis-nodes/commit/master
#
# SPDX-License-Identifier: GPL3
# License-Filename: LICENSE

import ast
import bpy
import sverchok
import sverchok_gis

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok_gis.utils import gis_loader

gpd_read_file = gis_loader.get_loader()

class SvSGNLoadGISData(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: load GIS data using parameters
    Tooltip: Import GPKG data
    """
    bl_idname = 'SvSGNLoadGISData'
    bl_label = 'Load GIS data'
    bl_icon = 'RNA'
    
    parameters : bpy.props.StringProperty(
        name="parameters", 
        default="{\"layer\": \"some_layer\"}", update=updateNode)

    def sv_init(self, context):
        self.width = 300
        self.inputs.new('SvFilePathSocket', "GPKG Path")
        self.inputs.new('SvStringsSocket', "parameters").prop_name = 'parameters'
        self.outputs.new('SvStringsSocket', "GIS data")

    def process(self):  
        
        if not gpd_read_file:
            # display on node that gpd has not been found.
            self.outputs["GIS data"].sv_set([[]])
            return

        # create initial variables      
        path = self.inputs[0].sv_get(deepcopy=False)
        parameters = self.inputs[1].sv_get(deepcopy=False)

        # ensure some kind of output even if nothing was found.
        gi = []
        gis_data = []

        if path:
            path = str(path[0][0])
        if parameters:
            parameters = ast.literal_eval(str(parameters[0][0]))

        if path:
            if not parameters:
                parameters = dict()

            gpd1 = gpd_read_file(path, **parameters)
            gi = gpd1.__geo_interface__
        
        gis_data.append(gi)
        self.outputs["GIS data"].sv_set(gis_data)
       
classes = [SvSGNLoadGISData]
register, unregister = bpy.utils.register_classes_factory(classes)
