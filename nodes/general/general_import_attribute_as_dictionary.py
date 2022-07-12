# This file is part of project Sverchok-gis. It's copyrighted by the contributors
# recorded in the version control history of the file, available from
# its original location https://github.com/Marcus-Richmond/sverchok-gis-nodes/commit/master
#
# SPDX-License-Identifier: GPL3
# License-Filename: LICENSE
DEBUG = True

import bpy
import sverchok
import sverchok_gis
import pandas as pd
from sverchok_gis.dependencies import geopandas as gpd

if gpd is None:

    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvSGNImportAttributeDict', 'Import Attribute as Dictionary', 'geopandas')
    classes = []

else:

    # import numpy as np
    from sverchok.node_tree import SverchCustomTreeNode
    from sverchok.data_structure import updateNode

    class SvSGNImportAttributeDict(SverchCustomTreeNode, bpy.types.Node):
        """
        Triggers: GIS import
        Tooltip: Import GPKG layer attributes as dictionary
        """
        bl_idname = 'SvSGNImportAttributeDict'  # should be add to `sverchok/index.md` file
        bl_label = 'Import Attribute as Dictionary Node'
        bl_icon = 'RNA'
        
        layer_name : bpy.props.StringProperty(name="layer name", default="some layer", update=updateNode)

        def sv_init(self, context):

            self.inputs.new('SvFilePathSocket', "GPKG Path")
            self.inputs.new('SvStringsSocket', "Layer Name").prop_name = 'layer_name'

            self.outputs.new("SvDictionarySocket", "Attribute Dict")

        def process(self):  
            
            # create initial variables for inputs 
            path = self.inputs["GPKG Path"].sv_get(deepcopy = False)
            layername = self.inputs["Layer Name"].sv_get(deepcopy = False)

            # ensure some kind of output even if nothing was found.
            attribute_dict = []
            if path:
                path = str(path[0][0])
            if layername:
                layername = str(layername[0][0])   # likely not necessary to cast to string.

            if path and layername:
                # read in gpkg layer as geopandas data frame, and make alias
                gpd1 = gpd.read_file(path, layer=layername)
                                
                # create data frame from geodataframe, by dropping geometry column
                df = pd.DataFrame(gpd1.drop(columns='geometry'))
                
                # convert data frame to dictionary
                df_dict = df.to_dict()

                # append dictionary            
                attribute_dict.append(df_dict)

            if DEBUG and path:

                if layername:
                    gpd1 = gpd.read_file(path, layer=layername)
                    gi = gpd1.__geo_interface__
                else:
                    gpd1 = gpd.read_file(path)
                    gi = gpd1.__geo_interface__

                if not hasattr(sverchok, 'gis_breakpoint'):
                    sverchok.gis_breakpoint = {}

                sverchok.gis_breakpoint = gi
                listAttribute = [gi]

            # set output dictionary as dictionary created above    
            self.outputs["Attribute Dict"].sv_set(attribute_dict)
       
    classes = [SvSGNImportAttributeDict]

register, unregister = sverchok_gis.utils.register_class_factory_deps(classes, deps=[gpd])
