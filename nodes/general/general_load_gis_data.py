# general_load_gis_data.py

# This file is part of project Sverchok-gis. It's copyrighted by the contributors
# recorded in the version control history of the file, available from
# its original location https://github.com/Marcus-Richmond/sverchok-gis-nodes/commit/master
#
# SPDX-License-Identifier: GPL3
# License-Filename: LICENSE

import bpy
import sverchok
import sverchok_gis

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok_gis.utils import gis_loader

gpd_read_file = gis_loader.get_loader()

class SvSGNLoadGISData(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: load GIS data
    Tooltip: Import GPKG layer
    """
    bl_idname = 'SvSGNImportAttribute'  # should be add to `sverchok/index.md` file
    bl_label = 'Import Attribute Node'
    bl_icon = 'RNA'
    
    key_name : bpy.props.StringProperty(name="key name", default="layer: some_layer", update=updateNode)

    def sv_init(self, context):
        self.inputs.new('SvFilePathSocket', "GPKG Path")
        self.inputs.new('SvStringsSocket', "Key Name").prop_name = 'key_name'
        self.outputs.new('SvStringsSocket', "GIS data")

    def process(self):  
        
        if not gpd_read_file:
            self.outputs["GIS data"].sv_set([[]])
            # display on node that gpd has not been found.
            return

        # create initial variables      
        path = self.inputs[0].sv_get(deepcopy=False)
        key_name = self.inputs[1].sv_get(deepcopy=False)

        # ensure some kind of output even if nothing was found.
        gi = []
        gis_data = []

        if path: path = str(path[0][0])
        if key_name: key_name = str(key_name[0][0])

        if path:
            if key_name:
                ...
            else:
                gpd1 = gpd_read_file(path, layer=layername)
                gi = gpd1.__geo_interface__

            gis_data.append(gi)
            
        self.outputs["GIS data"].sv_set(gis_data)
       
classes = [SvSGNLoadGISData]
register, unregister = bpy.utils.register_class_factory(classes)
