# This file is part of project Sverchok-gis. It's copyrighted by the contributors
# recorded in the version control history of the file, available from
# its original location https://github.com/Marcus-Richmond/sverchok-gis-nodes/commit/master
#
# SPDX-License-Identifier: GPL3
# License-Filename: LICENSE

import bpy

# import pandas as pd   # these are not strictly necessary i think for this node as defined
# import fiona
from sverchok_open3d.dependencies import geopandas as gpd

if gpd is None:

    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvSGNImportAttribute', 'Import Attribute', 'geopandas')

else:

    # import numpy as np
    from sverchok.node_tree import SverchCustomTreeNode
    from sverchok.data_structure import updateNode

    class SvSGNImportAttribute(SverchCustomTreeNode, bpy.types.Node):
        """
        Triggers: GIS import
        Tooltip: Import GPKG layer attribute
        """
        bl_idname = 'SvSGNImportAttribute'  # should be add to `sverchok/index.md` file
        bl_label = 'Import Attribute Node'
        bl_icon = 'RNA'
        
        layer_name : bpy.props.StringProperty(name="layer name", default="some layer", update=updateNode)
        attribute_name : bpy.props.StringProperty(name="attribute name", default="some_attribute", update=updateNode)

        def sv_init(self, context):

            self.inputs.new('SvFilePathSocket', "GPKG Path")
            self.inputs.new('SvStringsSocket', "Layer Name").prop_name = 'layer_name'
            self.inputs.new('SvStringsSocket', "Attribute Name").prop_name = 'attribute_name'
            
            self.outputs.new('SvStringsSocket', "Attribute Values")

        def process(self):  
            
            # create initial variables      
            path = self.inputs["GPKG Path"].sv_get(deepcopy = False)
            layername = self.inputs["Layer Name"].sv_get(deepcopy = False)
            attribute = self.inputs["Attribute Name"].sv_get(deepcopy = False)
            
            # ensure some kind of output even if nothing was found.
            listAttribute = []

            if path and layername and attribute:
                layername = str(self.layername[0][0])   # likely not necessary to cast to string.
                attribute = str(self.attribute[0][0])
                path = str(self.path[0][0])

                # read in gpkg layer as geopandas data frame, and make alias
                gpd1 = gpd.read_file(path, layer=layername)
                gi = gpd1.__geo_interface__

                # loop over gi to extract and collect attributes from feature properties.
                for features in range(len(gi['features'])):
                    value = [gi['features'][features]['properties'][attribute]]
                    listAttribute.append(value)
                
            self.outputs["Attribute Values"].sv_set(listAttribute)
       

def register():
    if o3d is not None: bpy.utils.register_class(SvSGNImportAttribute)

def unregister():
    if o3d is not None: bpy.utils.unregister_class(SvSGNImportAttribute)