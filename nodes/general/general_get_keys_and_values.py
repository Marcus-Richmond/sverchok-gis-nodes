# general_get_keys_and_values.py

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
# import pandas as pd   # these are not strictly necessary i think for this node as defined
# import fiona
from sverchok_gis.dependencies import geopandas as gpd


if gpd is None:

    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvSGNGetKeysAndValues', 'Get Keys and Values', 'geopandas')
    classes = []
else:

    # import numpy as np
    from sverchok.node_tree import SverchCustomTreeNode
    from sverchok.data_structure import updateNode

    class SvSGNGetKeysAndValues(SverchCustomTreeNode, bpy.types.Node):
        """
        Triggers: keys values
        Tooltip: Get Keys and Values from Stream
        """
        bl_idname = 'SvSGNGetKeysAndValues'
        bl_label = 'Get Keys and Values'
        bl_icon = 'RNA'
        
        def sv_init(self, context):
            self.inputs.new('SvStringsSocket', "Gis Stream")
            self.outputs.new('SvStringsSocket', "Keys")
            self.outputs.new('SvStringsSocket', "Values")

        def process(self):
            found_data = self.inputs[0].sv_get()
            keys_output, values_output = [], []

            if found_data:
                for dictionary in found_data:
                    keys_output.append(list(dictionary.keys()))
                    values_output.append(list(dictionary.values()))
                
            self.outputs["Keys"].sv_set(keys_output)
            self.outputs["Values"].sv_set(values_output)
       
    classes = [SvSGNGetKeysAndValues]

register, unregister = sverchok_gis.utils.register_class_factory_deps(classes, deps=[gpd])
